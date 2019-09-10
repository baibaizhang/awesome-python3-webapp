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
 

# 含dict的list排序并去重
def distinct(items,key, reverse=False):
    key = itemgetter(key)
    items = sorted(items, key=key, reverse=reverse)
    return [next(v) for _, v in groupby(items, key=key)]
 
def main():
    
    data_list = [{'日期': '2019-06-19', '获利比例': '41.15%', '亏损比例': '58.85%', '平均成本': '26.90', '90%成本': '24.00-31.17', '90成本集中度': '12.99%', '70%成本': '25.73-29.66', '70成本集中度': '7.09%'}, {'日期': '2019-07-02', '获利比例': '65.31%', '亏损比例': '34.69%', '平均成本': '27.02', '90%成本': '24.49-31.15', '90成本集中度': '11.98%', '70%成本': '25.95-29.55', '70成本集中度': '6.48%'}, {'日期': '2019-07-15', '获利比例': '82.64%', '亏损比例': '17.36%', '平均成本': '27.19', '90%成本': '25.51-31.12', '90成本集中度': '9.90%', '70%成本': '26.07-29.37', '70成本集中度': '5.95%'}, {'日期': '2019-07-29', '获利比例': '71.16%', '亏损比例': '28.84%', '平均成本': '27.57', '90%成本': '25.86-31.10', '90成本集中度': '9.20%', '70%成本': '26.27-29.64', '70成本集中度': '6.03%'}, {'日期': '2019-08-09', '获利比例': '13.85%', '亏损比例': '86.15%', '平均成本': '27.62', '90%成本': '25.84-31.12', '90成本集中度': '9.27%', '70%成本': '26.29-29.59', '70成本集中度': '5.91%'}, {'日期': '2019-08-22', '获利比例': '40.60%', '亏损比例': '59.40%', '平均成本': '27.62', '90%成本': '25.94-31.12', '90成本集中度': '9.08%', '70%成本': '26.38-29.59', '70成本集中度': '5.73%'}, {'日期': '2019-09-04', '获利比例': '30.97%', '亏损比例': '69.03%', '平均成本': '27.37', '90%成本': '25.84-31.12', '90成本集中度': '9.27%', '70%成本': '26.24-29.59', '70成本集中度':'6.01%'}]
    # new_list = distinct(data_list, '日期')
    new_list1 = distinct(data_list, '日期', True)
    # data_list.sort()
    # print(data_list)
    # print(new_list)
    print(new_list1)
 
 
if __name__ == '__main__':
    main()
	
	
	