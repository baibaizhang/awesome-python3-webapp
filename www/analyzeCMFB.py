#!/usr/bin/env python3
#coding:utf-8  
''''' 
@author: steve 
分析筹码分布数据
'''  


import requests,time,os,xlwt,xlrd,random
from CMFBData import CMFBData
from ExcelData import ExcelData


def get_url(code):
        codelist = {'60': 'sh', '00':'sz', '30':'sz'}
        for item in codelist:
            if code.startswith(item):
                return "http://quote.eastmoney.com/concept/" + codelist[item] + code + ".html"

def save_data(save_path, data_list):
    excel_data = ExcelData(save_path)
    try:
        excel_data.write_excel(data_list)
        print("数据已保存到文件： " + save_path)
    except FileNotFoundError:
        print(save_path + "----创建失败(上级目录不存在)")
        date = time.strftime('%Y%m%d%H%M%S')
        excel_data = ExcelData(date + ".xls")
        excel_data.write_excel(data_list)
        print("数据已保存到临时文件：" + os.getcwd() + '\\' + 'Data' + date + ".xls")
    except PermissionError:
        print(save_path + "----创建失败(文件已经被打开)")
        date = time.strftime('%Y%m%d%H%M%S')
        excel_data = ExcelData(date + ".xls")
        excel_data.write_excel(data_list)
        print("数据已保存到临时文件：" + os.getcwd() + '\\' + 'Data' + date + ".xls")

def collect_win_percent_stock(stock_list_path, save_path):
    # 读取股票列表
    data_path = stock_list_path #"D:\\pythonData\\股票数据\\TestData20190908.xls"  #文件的绝对路径
    get_data = ExcelData(data_path)                       #定义get_data对象, sheet名称默认Sheet1
    stock_list = get_data.read_excel()
    # 获取数据
    cmfb_data = CMFBData()
    win_list = []
    count = len(stock_list)
    index = 0
    percent = 0
    print("进度: " + "0%")
    for stock in stock_list:
        index = index + 1
        new_percent = index*100/count
        if new_percent > percent:
            print("进度: " + str(new_percent) + "%")
            percent = new_percent
        code = stock['code']
        name = stock['名称']
        data_current = cmfb_data.get_data_current(code)
        if not data_current: #为空就跳过
            continue
        stock['日期'] = data_current['日期']
        stock['获利比例'] = data_current['获利比例']
        stock['url'] = get_url(code)
        win_list.append(stock)
        
    # 保存结果到表格中
    #save_path = "D:\\pythonData\\分析数据\\WinTestData20190908.xls"
    save_data(save_path,win_list)


def main():
    date = time.strftime('%Y%m%d')
    # collect_win_percent_stock("D:\\pythonData\\股票数据\\深AData20190908.xls", "D:\\pythonData\\分析数据\\分析-深A"+'Data'+date+'.xls')
    # collect_win_percent_stock("D:\\pythonData\\股票数据\\中小板Data20190908.xls", "D:\\pythonData\\分析数据\\分析-中小板"+'Data'+date+'.xls')
    # collect_win_percent_stock("D:\\pythonData\\股票数据\\沪AData20190908.xls", "D:\\pythonData\\分析数据\\分析-沪A"+'Data'+date+'.xls')
    # collect_win_percent_stock("D:\\pythonData\\股票数据\\华为5G.xls", "D:\\pythonData\\分析数据\\分析-华为5G"+'Data'+date+'.xls')
    collect_win_percent_stock("D:\\pythonData\\股票数据\\TestData20190908.xls", "D:\\pythonData\\分析数据\\分析-TestData"+'Data'+date+'.xls')



 
if __name__ == '__main__':
    main()