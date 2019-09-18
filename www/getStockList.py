#!/usr/bin/env python3
#coding:utf-8  
''''' 
@author: steve 
get stock list

'''''  
from eastmoney import EastMoneyStockList
import os,shutil,time

def get_stock_list():
    east = EastMoneyStockList()
    save_path = 'D:\\PythonData\\stock\\list\\'+ 'hs_a_board'+ '.xls'
    bak_root_path = 'D:\\OneDrive\\stock\\list\\'
    
    east.get_stock_list('hs_a_board',save_path, except_code_list=['300','688']) #去除300，688开头的
    # east.get_stock_list('hs_a_board',save_path)
    date = time.strftime('%Y%m%d%H%M%S')
    if (os.path.exists(save_path)):
        bak_path = save_path[:-4]+ date + '.xls'
        shutil.copy(save_path, bak_path)
        shutil.copy(bak_path, bak_root_path)
    
if __name__ == '__main__':
    get_stock_list()



