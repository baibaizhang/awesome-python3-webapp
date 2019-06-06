'''
Created on 2018年2月11日

@author: Livon
'''
   
import urllib.request

import re
import pymysql

from urllib import request

# from stock.获取股票历史市值 import datetimeUtil
import datetimeUtil



def p( msg ):
    print( '%s - %s' % ( datetimeUtil.getDatetime(), msg ))



# 任务清单，每一次任务会领一份任务清单，清单中的第一项，是一个股票
# 任务：job - 大循环
# 目标：mission - 小目标
# missionList - 目标清单
# getMissionList
# 参数：tableName 表名
def getMissionList( tableName ):
    
    rowsCount = '5' ;    
    
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='password', db='stock', charset='utf8')
    # 创建游标
#     cursor = conn.cursor()

    cursor = conn.cursor()
    
#     sql='select * from '+ tableName +' where doneTime is NULL limit ' + rowsCount
    sql = 'select * from %s where doneTime is NULL limit %s' % ( tableName, rowsCount )
    cout = cursor.execute(sql)
#     print("数量： "+str(cout))
    rows = cursor.fetchall();
    
#     rows = conn.cursor().execute( sql ).fetchall()
    
#     for row in rows:
#         print("stockCode: "+str(row[0])+'  stockName： '+row[1]+"  startDate： "+ str(row[2]))
        
    cursor.close()
#     
#     try:
#         #获取一个游标
#         with conn.cursor() as cursor:
#             sql='select * from '+ tableName +' where doneTime is NULL limit 1'
#             cout=cursor.execute(sql)
#             print("数量： "+str(cout))
# 
#             for row in cursor.fetchall():
#                 #print('%s\t%s\t%s' %row)
#                 #注意int类型需要使用str函数转义
#                 print("stockCode: "+str(row[0])+'  stockName： '+row[1]+"  startDate： "+ str(row[2]))
# #         conn.commit()
# 
#     finally:
#         print( 'done' )
        
    
    cursor.close()
    conn.close()
    
#     print( datetimeUtil.getDatetime(), ' - 任务清单装载完毕！任务数量：', str( len( rows ))  )
#     print( '%s - %s missons loaded.' % ( datetimeUtil.getDatetime(), str( len( rows )) ) )
    p( '%s missons loaded.' % str( len( rows ) ))
    
    return rows




# 生成网址
def genUrl( row ):    
    
    stockCode = row[0]
    startDate = str( row[2] ).replace('-','')
#     endDate = ( row[3] == 'None' )? '': row[3]
#     endDate = ( row[3] == None ) and '' or row[3]
    endDate = ( row[3] == None ) and row[3] or ''
    dataSource = row[4]
#     True and "Fire" or "Water"  
#     print( row[3] is 'None')
#     print( row[3] is None )
#     print( row[3] is '' )
#     print( type( row[3] ) )
#     print( type( row[3] ) is None )
#     print( type( row[3] ) is 'NoneType' )
    
    url = 'http://quotes.money.163.com/service/chddata.html?code=%s%s&start=%s&end=%s'
    url = url % ( dataSource, stockCode, startDate, endDate )
    url += '&fields=LCLOSE;TOPEN;LOW;HIGH;TCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'    
    
    return url





def getCsv( url ):    
    
#     csv = csv.decode('gbk')
#     
#     csv_str = str(csv)
#     lines = csv_str.split("\\n")
#     
#     print( len( lines))
    
    return ''

# 从互联网上获取数据
def getStockDataList( url ):
    
    print( datetimeUtil.getDatetime(), ' - ', '准备从互联网获取数据 ...' )
    
#     http = urllib3.PoolManager()
#     r = http.request('GET', url )
#     url="http://www.example.com/"
#     headers={"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}

#     try:
#         req = urllib3.request(url, headers )
# #         req=urllib2.Request(url,headers=headers)
#         response = urllib3.request2.urlopen(req)
#     except urllib3.exceptions,e:
#         print e.reason
    dataList = None 
    try:
        response = request.urlopen( url )
        
        csv = response.read()     
        csv = csv.decode('gbk')  
    #     csv = csv.decode('iso-8859-1')        
        csv_str = str(csv)
        
#         print( type( csv ))
        
        if( len( csv_str ) < 1 ):
            print( '获取失败' )
        
#         print( csv_str )
    #     lines = csv_str.split("\\n")    
        lines = csv_str.splitlines()
#         print( '行数：' + str( len( lines )))   
        
        dataList = [] 
        
        for line in lines:
#             print( line )
            dataRow = line.split(',')
#             print( dataRow[0] )
            dataObj = {}
            dataObj['日期']       = dataRow[0]
            dataObj['股票代码']   = dataRow[1]
            dataObj['名称']       = dataRow[2]
            dataObj['前收盘']     = dataRow[3]
            dataObj['开盘价']     = dataRow[4]
            dataObj['最高价']     = dataRow[5]
            dataObj['最低价']     = dataRow[6]
            dataObj['收盘价']     = dataRow[7]
            dataObj['涨跌额']     = dataRow[8]
            dataObj['涨跌幅']     = dataRow[9]
            dataObj['换手率']     = dataRow[10]
            dataObj['成交量']     = dataRow[11]
            dataObj['成交金额']   = dataRow[12]
            dataObj['总市值']     = dataRow[13]
            dataObj['流通市值']   = dataRow[14]
            dataList.append(dataObj)
        
    except Exception as e:
        print( e )
        
    
    return dataList


def netEaseUrl( stockCode, startDate, endDate ):
    
    url = 'http://quotes.money.163.com/service/chddata.html?code=%s&start=%s&end=%s&fields='
    url = url % ( stockCode, startDate, endDate )
    
    print( url )
    
    return url

def receiveCsv( url ):
    
    # http://www.cnblogs.com/sysu-blackbear/p/3629420.html
    stockDataResponse = urllib.request.urlopen( url )
    stockData = stockDataResponse.read()
    # stockData = stockDataResponse.decode('utf8')
    stockData = stockData.decode('gb2312')
    # stockData = stockData.decode('gb2312')

#     print( stockData )
    
    return stockData


'''

'''
def getStockList():
    
    
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='stock', charset='utf8')
    # 创建游标
#     cursor = conn.cursor()
    
    try:
        #获取一个游标
        with conn.cursor() as cursor:
            sql='select * from stock_list'
            cout=cursor.execute(sql)
            print("数量： "+str(cout))

            for row in cursor.fetchall():
                #print('%s\t%s\t%s' %row)
                #注意int类型需要使用str函数转义
                print("stockCode: "+str(row[0])+'  stockName： '+row[1]+"  startDate： "+ str(row[2]))
#         conn.commit()

    finally:
        cursor.close()
        conn.close()


  
def dbStore( str_stocks ):
    
    
    print( type( str_stocks ))
        
    stocks = re.findall("\[(.*?)\]",str_stocks )
    stocks = re.findall("{(.*?)}",stocks[0])    
    
    # 创建连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='stock', charset='utf8')
    # 创建游标
    cursor = conn.cursor()
        
    for i in range( 0, len( stocks ) ):
        print( 'No.' + str(i))
        properties = stocks[i].split(',')            
#         print( properties )         
#         print( type( properties ))
#         effect_rows = insertDb( properties, cursor )
#         time.sleep(1)
        
    # 提交，不然无法保存新建或者修改的数据
    conn.commit()
  
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()    
    
    return ''


def updateJobList( jobListTable, row, insertedRows ):
    
    
    # 创建连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='stock', charset='utf8')
    # 创建游标
    cursor = conn.cursor()
#     otherStyletime == "2013-10-10 23:40:00"
    
#     sql ='update ' + jobListTable + ' set doneTime = "' + otherStyleTime + '" where stockCode = "' + row[0] + '"'
    
    sql = 'update %s set doneTime = "%s" , receivedRows = %s where stockCode = "%s"' % ( jobListTable, datetimeUtil.getDatetime(), insertedRows, row[0] )
    
    print( datetimeUtil.getDatetime(), ' - 更新任务清单：', sql )
    
    effect_row = cursor.execute( sql )
    
    conn.commit()  
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()    
    
    
    
def insertTable( dataList ):
    
    # 创建连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='stock', charset='utf8')
    # 创建游标
    cursor = conn.cursor()
        
    insertedRows = 0
    
    for i in range( 1, len( dataList )):
        
        for (k,v) in  dataList[i].items(): 
#             print( "dataList[i][%s]=" % k,v )
#             print( v )
            if( v == 'None' ):
#                 print('Change to NULL')
                dataList[i][k] = 'NULL'
        
#         for data in dataList[i]:
#             print( data. )
#             data = ( data == None ) and data or 'NULL'        
        
        sql = 'INSERT INTO stock_his_data ( '
        sql += '日期,'
        sql += '股票代码,'
        sql += '名称,'
        sql += '前收盘,'
        sql += '开盘价,'
        sql += '最低价,'
        sql += '最高价,'
        sql += '收盘价,'
        sql += '涨跌额,'
        sql += '涨跌幅,'
        sql += '换手率,'
        sql += '成交量,'
        sql += '成交金额,'
        sql += '总市值,'
        sql += '流通市值'   
        sql += ' ) '    
        sql += 'VALUES'  
        sql += ' ( '  
        
        sql += '"' + dataList[i]['日期']    +  '",'
        sql += '"' + dataList[i]['股票代码']+  '",'
        sql += '"' + dataList[i]['名称']    +  '",'
        sql +=       dataList[i]['前收盘']  +  ' ,'
        sql +=       dataList[i]['开盘价']  +  ' ,'
        sql +=       dataList[i]['最低价']  +  ' ,'
        sql +=       dataList[i]['最高价']  +  ' ,'
        sql +=       dataList[i]['收盘价']  +  ' ,'
        sql +=       dataList[i]['涨跌额']  +  ' ,'
        sql +=       dataList[i]['涨跌幅']  +  ' ,'
        sql +=       dataList[i]['换手率']  +  ' ,'
        sql +=       dataList[i]['成交量']  +  ' ,'
        sql +=       dataList[i]['成交金额']+  ' ,'
        sql +=       dataList[i]['总市值']  +  ' ,'
        sql +=       dataList[i]['流通市值']
        sql += ' ) '
        
#         print( sql )
        
        effect_row = cursor.execute( sql )
        
        if( effect_row > 0 ):
            insertedRows += 1
            
    print( datetimeUtil.getDatetime(), ' - 数据数量：', insertedRows )
#     
    # 提交，不然无法保存新建或者修改的数据
    conn.commit()  
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()    
    
    
    
#     arr_values = []
#     arr_columns = []
#     
#     for j in range( 0, len( properties) ):
#         
# #         print( 'propertie['+ str(j)+']: ' + properties[j] )
# #         key_value = properties[j].split(':')
# #         print( key_value[0] + ' -> ' + key_value[1] )
#         key = properties[j][:properties[j].find(':')]
#         value = properties[j][properties[j].find(':')+1:]
#         value = value.replace('"', '')
# #         print( key + ' -> ' + value )
# #         sql += '"' + value + '"'
#         arr_columns.append( '`' + key + '`' )
# #         arr_columns.append( key )
#         arr_values.append( '"' + value + '"' )
#         
#     sql = 'insert into stock_sina '
#     sql = sql + ' ( ' + ','.join( arr_columns ) + ' ) VALUES ( ' + ','.join( arr_values ) + ' ) '
    
#     print( sql )
       
#     effect_row = cursor.execute( sql )
    
    return insertedRows

        