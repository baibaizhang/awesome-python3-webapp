#!/usr/bin/env python3
#coding:utf-8  
''''' 
@author: steve 
get stock list

'''''  
from eastmoney import EastMoneyConcept
import os,shutil,time,zipfile

def get_cmfb_today_by_stock_list_path(stock_list_path, data_root_path, bak_root_path):
    east = EastMoneyConcept()
    east.get_today_by_stock_list_path(stock_list_path, data_root_path)
    date = time.strftime('%Y%m%d%H%M%S')
    # 压缩
    zip_file_name = data_root_path[:-1]+date+'.zip'
    print("压缩开始 :" + zip_file_name)
    make_zip(data_root_path, zip_file_name)
    print("压缩结束")
    # 备份
    # bak_root_path = bak_root_path[:-1] + '-bak-'+date
    print("备份开始 :" + bak_root_path)
    shutil.copy(zip_file_name, bak_root_path)
    # shutil.copytree(root_path, bak_root_path)
    print("备份结束")


#打包目录为zip文件
def make_zip(source_dir, output_filename):
    # zipf = zipfile.ZipFile(output_filename, 'w') #不压缩
    zipf = zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) #压缩
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)   #相对路径
            zipf.write(pathfile, arcname)
    zipf.close()

if __name__ == '__main__':
    # get_cmfb_today_by_stock_list_path('D:\\PythonData\\stock\\list\\hs_a_board.xls',\
    #                                   'D:\\PythonData\\stock\\data\\',\
    #                                   'D:\\OneDrive\\stock\\data\\' )
    get_cmfb_today_by_stock_list_path('D:\\PythonData\\stock\\list\\leak_list.xls',\
                                      'D:\\PythonData\\stock\\data\\',\
                                      'D:\\OneDrive\\stock\\data\\' )



