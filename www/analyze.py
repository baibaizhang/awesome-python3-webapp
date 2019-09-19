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
 
def get_url(code):
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
    leak_list = distinct(leak_list, 'code')
    excel_write = ExcelData(leak_path)
    excel_write.write_excel(leak_list)

def check_cmfb_exist_by_date(stock_list_path, stock_data_root_path, date, leak_path):
    excel_read = ExcelData(stock_list_path)
    stock_list = excel_read.read_excel()
    leak_list = []
    count = len(stock_list)
    index = 0
    for stock in stock_list:
        stock_data_path = stock_data_root_path + stock['code'] + '.xls'
        try:
            excel_cmfb = ExcelData(stock_data_path)
            data = excel_cmfb.read_excel_last_row()
        
            if data['日期'] != date:
                leak_list.append(stock)
                
            index += 1
            progress = format((index/count)*100, '.2f')+'%'
            print(progress)
        except:
            continue
    leak_list = distinct(leak_list, 'code')
    excel_write = ExcelData(leak_path)
    excel_write.write_excel(leak_list)

def analyze_cmfb(stock_list_path, stock_data_root_path, save_path):
    excel_read = ExcelData(stock_list_path)
    stock_list = excel_read.read_excel()
    analyze_data_list = []
    count = len(stock_list)
    index = 0
    for stock in stock_list:
        analyze_data = stock
        code = stock['code']
        if isinstance(code, float):
            code = str(code)
        try:
            stock_data_path = stock_data_root_path + code + '.xls'
            excel_cmfb = ExcelData(stock_data_path)
            data = excel_cmfb.read_excel_last_row() 
            analyze_data['日期'] = data['日期']
            analyze_data['获利比例'] = data['获利比例']
            analyze_data['平均成本'] = data['平均成本']
            analyze_data['收盘'] = data['收盘']
            analyze_data['url'] = get_url(code)
            analyze_data_list.append(analyze_data)
        except Exception as e:
            print(e)
        
        index += 1
        progress = format((index/count)*100, '.2f')+'%'
        print(progress)
    analyze_data_list = distinct(analyze_data_list, 'code')
    excel_write = ExcelData(save_path)
    excel_write.write_excel(analyze_data_list)
    print('文件以保存到：' + save_path)


def analyze_cmfg_5g():
    date = time.strftime('%Y-%m-%d')
    analyze_cmfb('D:\\PythonData\\stock\\list\\huawei5G.xls', \
                             'D:\\PythonData\\stock\\data\\', \
                             'D:\\PythonData\\stock\\analysis\\huawei5G'+ date + '.xls')

def analyze_cmfb_all():
    date = time.strftime('%Y-%m-%d')
    analyze_cmfb('D:\\PythonData\\stock\\list\\hs_a_board.xls', \
                            'D:\\PythonData\\stock\\data\\', \
                            'D:\\PythonData\\stock\\analysis\\hs_a_board'+ date + '.xls')

def analyze_cmfb_trace():
    date = time.strftime('%Y-%m-%d')
    analyze_cmfb('D:\\PythonData\\stock\\list\\trace.xls', \
                            'D:\\PythonData\\stock\\data\\', \
                            'D:\\PythonData\\stock\\analysis\\trace'+ date + '.xls')

def analyze_cmfb_performance_up():
    date = time.strftime('%Y-%m-%d')
    analyze_cmfb('D:\\PythonData\\stock\\list\\performance_up.xls', \
                            'D:\\PythonData\\stock\\data\\', \
                            'D:\\PythonData\\stock\\analysis\\performance_up'+ date + '.xls')

def main():
    date = time.strftime('%Y-%m-%d')
    # check('D:\\PythonData\\shontock\\list\\hs_a_board.xls', 'D:\\PythonData\\stock\\data\\', 'D:\\PytData\\shontock\\list\\leak.xls')
    # check_cmfb_exist_by_date('D:\\PythonData\\stock\\list\\hs_a_board.xls', \
    #                          'D:\\PythonData\\stock\\data\\', \
    #                          date, \
    #                          'D:\\PythonData\\stock\\list\\leak_by_date'+ date + '.xls')
    # analyze_cmfb_all()
    # analyze_cmfg_5g()
    analyze_cmfb_performance_up()
    # analyze_cmfb_trace()


'''
分析最近的一次成交额大于前面n天的平均成交额的倍数
:param stock_list_path  列表文件路径
:param stock_data_root_path 所有数据路径
:param save_path 分析完后数据保存的路径
:param before_days  前面n天
:param rate  倍数，浮点数，可以为0.x倍
'''
def analyse_volume(stock_list_path, stock_data_root_path, save_path, before_days, rate):
    excel_read = ExcelData(stock_list_path)
    stock_list = excel_read.read_excel()
    analyze_data_list = []
    count = len(stock_list)
    index = 0
    for stock in stock_list:
        analyze_data = stock
        code = stock['code']
        if isinstance(code, float):
            code = str(code)
        try:
            stock_data_path = stock_data_root_path + code + '.xls'
            excel_cmfb = ExcelData(stock_data_path)
            data_list = excel_cmfb.read_excel_last_n_row(before_days+1) 

            # TODO
            analyze_data['日期'] = data['日期']
            analyze_data['获利比例'] = data['获利比例']
            analyze_data['平均成本'] = data['平均成本']
            analyze_data['收盘'] = data['收盘']
            analyze_data['url'] = get_url(code)
            analyze_data_list.append(analyze_data)
        except Exception as e:
            print(e)
        
        index += 1
        progress = format((index/count)*100, '.2f')+'%'
        print(progress)
    analyze_data_list = distinct(analyze_data_list, 'code')
    excel_write = ExcelData(save_path)
    excel_write.write_excel(analyze_data_list)
    print('文件以保存到：' + save_path)
    
 

if __name__ == '__main__':
    main()
	
	
	