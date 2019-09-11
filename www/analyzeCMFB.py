#!/usr/bin/env python3
#coding:utf-8  
''''' 
@author: steve 
分析筹码分布数据
'''  


import requests,time,os,xlwt,xlrd,random
from CMFBData import CMFBData
from ExcelData import ExcelData
from multiprocessing import Process, Queue, Pool
from eastmoney import EastMoneyConcept




def get_url(code):
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
        data_current = cmfb_data.get_current(code)
        if not data_current: #为空就跳过
            continue
        stock['日期'] = data_current['日期']
        stock['获利比例'] = data_current['获利比例']
        stock['url'] = get_url(code)
        win_list.append(stock)
        
    # 保存结果到表格中
    #save_path = "D:\\pythonData\\分析数据\\WinTestData20190908.xls"
    save_data(save_path,win_list)

def get_cmfb_data_today(stock):
    concept = EastMoneyConcept(stock)
    cmfb_data = concept.parse_page_cmfb_today()
    return cmfb_data
    # print(cmfb_data)
    # q.put(cmfb_data)


def get_cmfb_data_today_from_stocklist(stock_list_path, save_path):
    # 创建一个队列用来保存进程获取到的数据
    q= Queue(10)
    result = []
    # 读取股票列表
    excel = ExcelData(stock_list_path)                       #定义get_data对象, sheet名称默认Sheet1
    # stock_list = excel.read_excel()
    # stock_list = [{'code':'000002'},{'code':'000001'},{'code':'000004'}]
    stock_list = ['000002','000001','000004']

    pool = Pool(4)
    # pool.map(get_cmfb_data_today, stock_list)
    for stock in stock_list:
        data = pool.apply_async(get_cmfb_data_today,args=(stock,))
        # result.append(data)

    # print(cmfb_list)
    
    
    pool.close()
    pool.join()

    # for res in result:
    #     print(res.get())
    # # 保存进程
    # Process_list = []
    # # 创建并启动进程
    # for stock in stock_list:
    #     # p = EastMoneyConcept(stock['code'],q)
    #     p = EastMoneyConcept(stock,q)
    #     p.start()
    #     Process_list.append(p)
    
    # # 让主进程等待子进程执行完成
    # for i in Process_list:
    #     i.join()

    print("process finish")
    # while not q.empty():
    #     print(q.get())

def main():
    # date = time.strftime('%Y%m%d')
    # # collect_win_percent_stock("D:\\pythonData\\股票数据\\深AData20190908.xls", "D:\\pythonData\\分析数据\\分析-深A"+'Data'+date+'.xls')
    # # collect_win_percent_stock("D:\\pythonData\\股票数据\\中小板Data20190908.xls", "D:\\pythonData\\分析数据\\分析-中小板"+'Data'+date+'.xls')
    # # collect_win_percent_stock("D:\\pythonData\\股票数据\\沪AData20190908.xls", "D:\\pythonData\\分析数据\\分析-沪A"+'Data'+date+'.xls')
    # # collect_win_percent_stock("D:\\pythonData\\股票数据\\华为5G.xls", "D:\\pythonData\\分析数据\\分析-华为5G"+'Data'+date+'.xls')
    # collect_win_percent_stock("D:\\pythonData\\股票数据\\TestData20190908.xls", "D:\\pythonData\\分析数据\\分析-TestData"+'Data'+date+'.xls')
    get_cmfb_data_today_from_stocklist("D:\\pythonData\\股票数据\\深AData20190911.xls","")

    
 
if __name__ == '__main__':
    main()