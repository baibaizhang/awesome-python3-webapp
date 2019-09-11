#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''''' 
@author: steve 
从东方财富网获取股票列表数据
'''  
 
import requests,time,os,xlwt,xlrd,random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from ExcelData import ExcelData
from multiprocessing import Process, Queue
 

class EastMoney(): 
    def _init_browser(self):
        # 给浏览器设置属性
        option = webdriver.ChromeOptions()
        # 设置默认隐藏，后台运行
        option.add_argument("headless")
        # 产生随机user-agent
        option.add_argument(UserAgent().random)
        return webdriver.Chrome(options=option)

    def _request_url(self, browser, url):
        retry_time = 0
        while retry_time <= 3:
            try:
                print("请求url:"+url)
                browser.get(url)
                return True
            except Exception as e:
                print("%s%s" % (e,url))
                retry_time = retry_time + 1
        return False

class EastMoneyStockList(EastMoney):
    def __init__(self, market_name):
        self._market_name = market_name

    def _get_url(self, market_name):
        market_list = {'沪深A股':'http://quote.eastmoney.com/center/gridlist.html#hs_a_board'\
                    ,'上证A股':'http://quote.eastmoney.com/center/gridlist.html#hs_a_board'\
                    ,'深圳A股':'http://quote.eastmoney.com/center/gridlist.html#sz_a_board'\
                    ,'中小板':'http://quote.eastmoney.com/center/gridlist.html#sme_board'\
                    ,'创业板':'http://quote.eastmoney.com/center/gridlist.html#gem_board'\
                    ,'科创板':'http://quote.eastmoney.com/center/gridlist.html#kcb_board'}
        return market_list[market_name]

    def parse_page(self):
        stock_list = []
        url = self._get_url(self._market_name)
        #启动浏览器
        browser = self._init_browser() 
        if not self._request_url(browser,url):
            return stock_list

        while True:
            # 等待list加载完成，不然抓取不到数据
            wait = WebDriverWait(browser, 10)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='listview full']" )))

            # 解析网页
            soup = BeautifulSoup(browser.page_source, 'lxml')

            for tr in soup.find('div',class_='listview full').find('tbody').find_all('tr'):
                stock = {}
                span = tr.find('span')
                if span.contents[0] == '-':
                    continue
                a = tr.findAll('a')
                stock['code'] = a[0].contents[0]
                stock['名称'] = a[1].contents[0]

                stock_list.append(stock)
                print(stock)

            # 查找目标按钮
            try:
                btn_next = browser.find_element_by_xpath("//a[@class='next paginate_button']")
                btn_next.click()
                time.sleep(random.randint(1,2)+random.random()) #随机延时?.?s  以防封IP
            except NoSuchElementException:
                # print(e.msg)
                break

        #关闭浏览器          
        browser.quit()   
        # 按照code从小到大排序
        stock_list.sort(key=lambda k: (k.get('code', 0)))
        return stock_list

class EastMoneyConcept(EastMoney, Process):
    def __init__(self, code, q = Queue()):
        # 重写写父类的__init__方法
        super(EastMoneyConcept, self).__init__()
        self._code = code
        self._q = q

    def _get_url(self, code):
        code_map = {'60': 'sh', '00':'sz', '30':'sz'}
        code_str = ''
        if isinstance(code, int):
            code_str = str(code)
        elif isinstance(code, float):
            code_str = str(code)
        elif isinstance(code, str):
            code_str = code
        for item in code_map:
            if code_str.startswith(item):
                return "http://quote.eastmoney.com/concept/" + code_map[item] + code_str + ".html"
   
    def _pre_load(self,browser):
        try:
            # 找到筹码分布的按钮---通过xpath
            btn_cmfb_xpath = "//a[text()='筹码分布']"
            # 等待响应完成
            wait = WebDriverWait(browser, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, btn_cmfb_xpath)))
            # 查找目标按钮
            btn_cmfb = browser.find_element_by_xpath(btn_cmfb_xpath)
            # 找到按钮后单击
            btn_cmfb.click()

            # 等待筹码分布的元素显示出来，不然解析数据的时候抓取不到相关数据
            wait = WebDriverWait(browser, 10)
            # wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='__emchatrs3_cmfb']" )))
            # wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='__emchatrs3_cmfb']" )))
            wait.until(EC.text_to_be_present_in_element((By.XPATH,"//div[@class='__emchatrs3_cmfb']"),u'集中度'))
            return True
        except Exception as e:
            print("%s" % (e))
            return False

    def parse_page_cmfb_today(self):
        cmfb_data = {}
        url = self._get_url(self._code)
        browser = self._init_browser()
        if not self._request_url(browser,url):
            return cmfb_data
        if not self._pre_load(browser):
            return cmfb_data
        
        cmfb_data = self._parse_page_cmfb_data(browser)
        browser.quit()
        return cmfb_data

    def run(self):
        data = self.parse_page_cmfb_today()
        self._q.put(data)

    # 解析网页获取筹码分布数据并返回数据
    def _parse_page_cmfb_data(self, browser):
        COLUMN_LIST = ('日期','获利比例','亏损比例','平均成本','90%成本','90成本集中度','70%成本','70成本集中度')
        count = len(COLUMN_LIST)
        data = {}
        index = 0
        # 解析网页
        soup = BeautifulSoup(browser.page_source, 'lxml')
        for span in soup.find(class_="__emchatrs3_cmfb").find_all('span'):
            if index >= count:
                break
            data[COLUMN_LIST[index]] = span.contents[0]
            index = index + 1

        print(data)   
        return data

    #爬虫获取数据
    # def _get_data(self):
    #     print("get data from " + self._url)
    #     data_list = []

    #     time.sleep(random.randint(1,5)+random.random()) #随机延时?.?s  以防封IP

    #     # 这里经常出现加载超的异常，后面需要处理一下：捕获异常后，刷新浏览器
    #     browser = self._browser
    #     browser.get(self._url)

    #     while True:
    #         # 等待筹码分布的元素显示出来，不然解析数据的时候抓取不到相关数据
    #         wait = WebDriverWait(browser, 10)
    #         wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='listview full']" )))

    #         # 解析网页
    #         soup = BeautifulSoup(browser.page_source, 'lxml')

    #         for tr in soup.find('div',class_='listview full').find('tbody').find_all('tr'):
    #             stock = {}
    #             span = tr.find('span')
    #             if span.contents[0] == '-':
    #                 continue
    #             a = tr.findAll('a')
    #             stock['code'] = a[0].contents[0]
    #             stock['名称'] = a[1].contents[0]

    #             data_list.append(stock)
    #             print(stock)

    #         # 查找目标按钮
    #         try:
    #             btn_next = browser.find_element_by_xpath("//a[@class='next paginate_button']")
    #             btn_next.click()
    #             time.sleep(random.randint(1,2)+random.random()) #随机延时?.?s  以防封IP
    #         except NoSuchElementException:
    #             # print(e.msg)
    #             break    
    #     # 按照code从小到大排序
    #     data_list.sort(key=lambda k: (k.get('code', 0)))
    #     return data_list
    #     # self.write_excel(Data,Record)#数据写入excel

    # def _save_data(self, data_list):
    #     excel_data = ExcelData(self._save_path)
    #     try:
    #         excel_data.write_excel(data_list)
    #         print("数据已保存到文件： " + self._save_path)
    #     except FileNotFoundError:
    #         print(self._save_path + "----创建失败(上级目录不存在)")
    #         date = time.strftime('%Y%m%d%H%M%S')
    #         excel_data = ExcelData(date + ".xls")
    #         excel_data.write_excel(data_list)
    #         print("数据已保存到临时文件：" + os.getcwd() + '\\' + 'Data' + date + ".xls")
    #     except PermissionError:
    #         print(self._save_path + "----创建失败(文件已经被打开)")
    #         date = time.strftime('%Y%m%d%H%M%S')
    #         excel_data = ExcelData(date + ".xls")
    #         excel_data.write_excel(data_list)
    #         print("数据已保存到临时文件：" + os.getcwd() + '\\' + 'Data' + date + ".xls")
        

       
    # def run(self):
    #     data_list = self._get_data()
    #     self._save_data(data_list)
        
 
 
def main():
    date = time.strftime('%Y%m%d')

    # east_stock_list = EastMoneyStockList('科创板')
    # stock_list = east_stock_list.parse_page()
    # print(stock_list)

    concept = EastMoneyConcept('000002')
    concept.parse_page_cmfb_today()
    # # 获取科创板所有股票列表
    # url = "http://quote.eastmoney.com/center/gridlist.html#sz_a_board"
    # save_path = 'D:\\pythonData\\股票数据\\'+"深A" + 'Data'+date+'.xls'
    # test = East(url,save_path)
    # test.run()
    
    # 获取A股所有股票列表
    # url = "http://quote.eastmoney.com/center/gridlist.html#hs_a_board"
    # save_path = 'D:\\pythonData\\股票数据\\'+"沪深A股" + 'Data'+date+'.xls'
    # test = East(url,save_path)
    # test.run()   
 
 
 
if __name__ == '__main__':
    main()
	
	
	