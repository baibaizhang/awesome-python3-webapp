#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
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
        self.Data = []
        self.Date = time.strftime('%Y%m%d')
        self.Record = 'D:\\pythonData\\股票数据\\'+'Data'+self.Date+'.xls'
        print (self.Record)
        # 给浏览器设置属性
        option = webdriver.ChromeOptions()
        # 设置默认隐藏，后台运行
        option.add_argument("headless")
        # 产生随机user-agent
        option.add_argument(UserAgent().random)
        
        self.browser = webdriver.Chrome(options=option)
        # if os.path.exists(self.Record):
        #     print ('Record exist...')
        # else:
        #     print ('Get data ...')
        #     self.get_data()
 
 
 
    #爬虫获取数据
    def get_data(self, url):
        time.sleep(random.randint(1,5)+random.random()) #随机延时?.?s  以防封IP
 
        # 这里经常出现加载超的异常，后面需要处理一下：捕获异常后，刷新浏览器
        browser = self.browser
        browser.get(url)

        record_d = []
        while True:
            # 等待筹码分布的元素显示出来，不然解析数据的时候抓取不到相关数据
            wait = WebDriverWait(browser, 10)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='listview full']" )))

            # 解析网页
            soup = BeautifulSoup(browser.page_source, 'lxml')

            # for a in soup.find('div',class_='listview full').find_all('a'):
            #     try:
            #         num = a.contents[0]
            #     except IndexError as e:
            #         continue
       
            #     if (len(num) == 6) and (num.startswith('00') or num.startswith('60') or num.startswith('30')):
            #         pass
            #     else:
            #         continue
            #     print(num)
            #     record_d.append(num)

            for tr in soup.find('div',class_='listview full').find('tbody').find_all('tr'):
                stock = {}
                a = tr.findAll('a')
                stock['code'] = a[0].contents[0]
                stock['名称'] = a[1].contents[0]
                print(stock)

            break
                # try:
                #     num = a.contents[0]
                # except IndexError as e:
                #     continue
       
                # if (len(num) == 6) and (num.startswith('00') or num.startswith('60') or num.startswith('30')):
                #     pass
                # else:
                #     continue
                # print(num)
                # record_d.append(num)

            # 查找目标按钮
            try:
                btn_next = browser.find_element_by_xpath("//a[@class='next paginate_button']")
                btn_next.click()
                time.sleep(random.randint(1,2)+random.random()) #随机延时?.?s  以防封IP
            except NoSuchElementException as e:
                break       
        
        record_d.sort()
        
        print(len(record_d))

        print(record_d)
        print(record_d[-1])
 
 
 
def main():
    test = East()
    # test.get_data("http://quote.eastmoney.com/center/gridlist.html#sz_a_board")
    test.get_data("http://quote.eastmoney.com/center/gridlist.html#sh_a_board")
 
 
 
if __name__ == '__main__':
    main()
	
	
	