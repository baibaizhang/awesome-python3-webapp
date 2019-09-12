#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''''' 
@author: steve 

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
from multiprocessing import Process, Queue, Pool
import multiprocessing as mp
import threadpool  
from multiprocessing import cpu_count


def init_browser():
    # 给浏览器设置属性
    option = webdriver.ChromeOptions()
    # 设置默认隐藏，后台运行
    option.add_argument("headless")
    # 产生随机user-agent
    option.add_argument(UserAgent().random)
    return webdriver.Chrome(options=option)

def request_url(url):
    browser = init_browser()
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

def code2url(code):
    code_map = {'60': 'sh', '00':'sz', '30':'sz', '688':'sh'}
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

def pre_load(browser):
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

            # # 等待筹码分布的元素显示出来，不然解析数据的时候抓取不到相关数据
            # wait = WebDriverWait(browser, 10)
            # # wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='__emchatrs3_cmfb']" )))
            # # wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='__emchatrs3_cmfb']" )))
            # wait.until(EC.text_to_be_present_in_element((By.XPATH,"//div[@class='__emchatrs3_cmfb']"),u'集中度'))
            return True
        except Exception as e:
            print("%s" % (e))
            return False

def request_by_code(browser, stock):
    code = stock['code']
    url = code2url(code)
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

def parse_page_cmfb_data(browser):
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
    

def get_cmfb_data_today_by_stock(stock):
    browser = init_browser()
    request_by_code(browser, stock)
    pre_load(browser)
    # parse_page_cmfb_data(browser)
    # browser.close() #关闭当前窗口
    browser.quit()  #关闭所有窗口

def test_processpool(stock_list, num_process):
    pool = mp.Pool(processes=num_process) #即一次只能同时处理3个请求
    start_time = time.time()
    for stock in stock_list:
        pool.apply_async(get_cmfb_data_today_by_stock,(stock,))       
    print ("The main's mark")
    pool.close()
    pool.join()
    print('%d second'% (time.time()-start_time))

def test_threadpool(stock_list, num_thread):
    pool = threadpool.ThreadPool(num_workers = num_thread) 
    start_time = time.time()
    requests = threadpool.makeRequests(get_cmfb_data_today_by_stock, stock_list) 
    [pool.putRequest(req) for req in requests] 
    pool.wait() 
    print('%d second'% (time.time()-start_time))

def main():
    # urls = ['http://quote.eastmoney.com/concept/sz000002.html']
    # urls = ['http://quote.eastmoney.com/concept/sz000002.html','http://quote.eastmoney.com/concept/sz000001.html']
    
    stock_list_path = "D:\\pythonData\\kcb_Data20190909.xls"
    excel = ExcelData(stock_list_path) 
    stock_list = excel.read_excel()
    cpu_num = cpu_count()
    print("cpu num : %d" % cpu_num)
    # code_list = ['000001','000002']
    # test_processpool(stock_list, (cpu_num - 2))
    test_processpool(stock_list, 2)
    # test_threadpool(stock_list, 4)
    # test_threadpool(stock_list, 20)
    # test_threadpool(stock_list, 30)

if __name__ == '__main__':
    main()