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

from operator import itemgetter
from itertools import groupby
from ExcelData import ExcelData

# 含dict的list排序并去重
def distinct(items,key, reverse=False):
    key = itemgetter(key)
    items = sorted(items, key=key, reverse=reverse)
    return [next(v) for _, v in groupby(items, key=key)]
 

def check(stock_list_path, stock_data_root_path, leak_path):
    excel_read = ExcelData(stock_list_path)
    stock_list = excel_read.read_excel()
    leak_list = []
    for stock in stock_list:
        stock_data_path = stock_data_root_path + stock['code'] + '.xls'
        if os.path.exists(stock_data_path):
            continue
        else:
            leak_list.append(stock)
    
    excel_write = ExcelData(leak_path)
    excel_write.write_excel(leak_list)



def main():
    check('D:\\pythonData\\股票列表\\沪深A股Data20190916.xls', 'D:\\pythonData\\股票数据\\', 'D:\\pythonData\\股票列表\\leak.xls')


    
 

if __name__ == '__main__':
    main()
	
	
	