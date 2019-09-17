#!/usr/bin/env python3
#coding:utf-8  
''''' 
@author: steve 
get stock list

'''''  
from eastmoney import EastMoneyConcept
import os,shutil,time,zipfile

def get_cmfb_today_by_stock_list_path(stock_list_path, root_path):
    date = time.strftime('%Y%m%d%H%M%S')
    # bak_root_path = root_path[:-1] + '-bak-'+date
    # print("备份开始 :" + bak_root_path)
    # shutil.copytree(root_path, bak_root_path)
    # print("备份结束 :" + bak_root_path)
    zip_file_name = root_path[:-1]+date+'.zip'
    print("备份压缩开始 :" + zip_file_name)
    make_zip(root_path, zip_file_name)
    print("备份压缩结束 :" + zip_file_name)
    east = EastMoneyConcept()
    east.get_today_by_stock_list_path(stock_list_path, root_path)

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
    get_cmfb_today_by_stock_list_path('D:\\OneDrive\\stock\\list\\hs_a_board.xls', 'D:\\OneDrive\\stock\\data\\')



