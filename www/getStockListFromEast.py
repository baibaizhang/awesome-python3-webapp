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
 
class East(object):
    def __init__(self):
        # 给浏览器设置属性
        option = webdriver.ChromeOptions()
        # 设置默认隐藏，后台运行
        option.add_argument("headless")
        # 产生随机user-agent
        option.add_argument(UserAgent().random)
        
        self.browser = webdriver.Chrome(options=option)
 
    def __del__(self):
        # 关闭浏览器
        self.browser.quit()
        print(self.__class__.__name__+" __del__")
 
    def write_excel(self,Data,Record):
        lis=Data
        listkeys = lis[0].keys()  # 找到所有的键值
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('sheet 1')
        number = 0
 
        for key in list(listkeys):  # 键值需要强制转换成list类型
            sheet.write(0, number, key)
            number = number + 1
 
        x = 1
        for one_dict in lis:  # 遍历列表中所有的字典
            y = 0
            for key in list(listkeys):  # 找到所有键值对应的数据
                sheet.write(x, y, one_dict[key])  # 存入
                y = y + 1
            x = x + 1
 
        wbk.save(Record[:-3]+'xls')#保存文件
    
    #爬虫获取数据
    def get_data(self, url, prefix=''):
        Data = []
        Date = time.strftime('%Y%m%d')
        Record = 'D:\\pythonData\\股票数据\\'+prefix+'Data'+Date+'.xls'
        print (Record)

        if os.path.exists(Record):
            print ('Record exist...')
            return
        else:
            print ('Get data ...')

        time.sleep(random.randint(1,5)+random.random()) #随机延时?.?s  以防封IP

        # 这里经常出现加载超的异常，后面需要处理一下：捕获异常后，刷新浏览器
        browser = self.browser
        browser.get(url)

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

                Data.append(stock)
                print(stock)

            # 查找目标按钮
            try:
                btn_next = browser.find_element_by_xpath("//a[@class='next paginate_button']")
                btn_next.click()
                time.sleep(random.randint(1,2)+random.random()) #随机延时?.?s  以防封IP
            except NoSuchElementException as e:
                break    

        Data.sort(key=lambda k: (k.get('code', 0)))
        self.write_excel(Data,Record)#数据写入excel
 
 
 
def main():
    test = East()
    # test.get_data("http://quote.eastmoney.com/center/gridlist.html#kcb_board","科创板")
    test.get_data("http://quote.eastmoney.com/center/gridlist.html#hs_a_board","沪深A股")
 
 
 
if __name__ == '__main__':
    main()
	
	
	