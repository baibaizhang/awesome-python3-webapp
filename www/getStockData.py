'''
《获取股票历史市值》
Created on 2018年2月12日
@author: Livon

# 读取 股票列表，含代码及 上市日期、终止上市日期

（1）列表
        每次执行前，手工新建一个当前日期的表，如果存在就删除重建（可能是执行一个存储过程）
        表名：stock_list_20180212 // 股票列表
        表字段：id, 股票代码， 是否顺利完成，获取记录数量
        每次取一条记录，依次执行，中断了，下次可以从中断处继续。
        
（2）
每条记录，按指定日期范围进行获取

再建

# 从网易数据接口拉取市值数据

# 存入表 stock_his_marketCap 中

'''

import util
import urllib
import csv
import time
import datetimeUtil

from urllib import request

jobListTable = 'stock_list_20180209'

def p( msg ):
    print( '%s - %s' % ( datetimeUtil.getDatetime(), msg ))

def startJob():

    # 从数据池中读取 n 记录
    missionList = util.getMissionList( jobListTable )
    
    # 循环处理上述的 n 条记录
    for mission in missionList:
#         for value in row:
#             print( value )
        # 根据记录生成一条 url，一个 url 可以获取几千条日记录
        url = util.genUrl( mission )
    #     url = 'http://quotes.money.163.com/service/chddata.html?code=1000001&start=19910401&end=19910409'
    #     url += '&fields=LCLOSE;TOPEN;HIGH;LOW;TCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'  
                
#         print( dt(), ' - ', url )
        p( 'url: %s' % url )
        
        # 从互联网上获取股票数据
        dataList = util.getStockDataList( url )
        print(dataList)
        
        if( dataList != None ):
            # 将数据保存在目标表：股票历史数据表中
            insertedRows = util.insertTable( dataList )        
            # 更新 mission List 状态标志列
            util.updateJobList( jobListTable, mission, insertedRows )    
        else :
            p( 'csv 文件无数据。' )
        
        p('standby a moment for next mission（ you can terminal the program at this time）.')
        time.sleep(3)
        
# main
for i in range( 0, 2 ):
    p( 'startJob: %s' % str(i)  )
    startJob()
    
# done
print( '= = = = = = = = = = = = = = = = = = = = = = ' )
p( 'all done !')
print( '= = = = = = = = = = = = = = = = = = = = = = ' )
