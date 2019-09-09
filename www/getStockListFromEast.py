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
 
class East(object):
    def __init__(self, url, save_path):
        # 给浏览器设置属性
        option = webdriver.ChromeOptions()
        # 设置默认隐藏，后台运行
        option.add_argument("headless")
        # 产生随机user-agent
        option.add_argument(UserAgent().random)
        
        self._browser = webdriver.Chrome(options=option)
        self._url = url
        self._save_path = save_path
 
    def __del__(self):
        # 关闭浏览器
        self._browser.quit()
        print(self.__class__.__name__+" __del__")

    #爬虫获取数据
    def _get_data(self):
        print("get data from " + self._url)
        data_list = []

        time.sleep(random.randint(1,5)+random.random()) #随机延时?.?s  以防封IP

        # 这里经常出现加载超的异常，后面需要处理一下：捕获异常后，刷新浏览器
        browser = self._browser
        browser.get(self._url)

        while True:
            # 等待筹码分布的元素显示出来，不然解析数据的时候抓取不到相关数据
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

                data_list.append(stock)
                print(stock)

            # 查找目标按钮
            try:
                btn_next = browser.find_element_by_xpath("//a[@class='next paginate_button']")
                btn_next.click()
                time.sleep(random.randint(1,2)+random.random()) #随机延时?.?s  以防封IP
            except NoSuchElementException:
                # print(e.msg)
                break    
        # 按照code从小到大排序
        data_list.sort(key=lambda k: (k.get('code', 0)))
        return data_list
        # self.write_excel(Data,Record)#数据写入excel

    def _save_data(self, data_list):
        excel_data = ExcelData(self._save_path)
        try:
            excel_data.write_excel(data_list)
            print("数据已保存到文件： " + self._save_path)
        except FileNotFoundError:
            print(self._save_path + "----创建失败(上级目录不存在)")
            date = time.strftime('%Y%m%d%H%M%S')
            excel_data = ExcelData(date + ".xls")
            excel_data.write_excel(data_list)
            print("数据已保存到临时文件：" + os.getcwd() + '\\' + 'Data' + date + ".xls")
        except PermissionError:
            print(self._save_path + "----创建失败(文件已经被打开)")
            date = time.strftime('%Y%m%d%H%M%S')
            excel_data = ExcelData(date + ".xls")
            excel_data.write_excel(data_list)
            print("数据已保存到临时文件：" + os.getcwd() + '\\' + 'Data' + date + ".xls")
        

       
    def run(self):
        data_list = self._get_data()
        self._save_data(data_list)
        
 
 
def main():
    date = time.strftime('%Y%m%d')

    # 获取科创板所有股票列表
    url = "http://quote.eastmoney.com/center/gridlist.html#kcb_board"
    save_path = 'D:\\pythonData\\股票数据\\'+"科创板" + 'Data'+date+'.xls'
    test = East(url,save_path)
    test.run()
    
    # 获取A股所有股票列表
    # url = "http://quote.eastmoney.com/center/gridlist.html#hs_a_board"
    # save_path = 'D:\\pythonData\\股票数据\\'+"沪深A股" + 'Data'+date+'.xls'
    # test = East(url,save_path)
    # test.run()   
 
 
 
if __name__ == '__main__':
    main()
	
	
	