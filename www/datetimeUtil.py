'''
Created on 2018年2月14日

@author: Livon
'''

import time

def getDatetime():
    
    timeArray = time.localtime( time.time() )
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    
    return otherStyleTime