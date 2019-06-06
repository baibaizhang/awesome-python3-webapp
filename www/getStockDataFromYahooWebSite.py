#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'steve'

'''

'''

import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import requests
import time,datetime
import json
from bs4 import BeautifulSoup



def ohlc_hist(tickCode, start_date, end_date, frequency):

    start_date = int(datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end_date = int(datetime.datetime.strptime(end_date, "%Y-%m-%d").timestamp())

    tick_suffix_dict = {'SH':'SS','SZ':'SZ','HK':'HK'}

    freq_dict = {"D":"1d",  "w":"1wk",  "m":"1mo" }

    url = "https://finance.yahoo.com/quote/{}/history?period1={}&period2={}&interval={}&filter=history&frequency={}".\
    format(tickCode,start_date,end_date,frequency,frequency)

    # 从网页上获取JSON数据
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"lxml" )
    script1 = soup.find_all('script')
    script2 = script1[-3]
    script3 = script2.text
    script4 = script3.split("\n")
    script_json = json.loads(soup.find_all('script')[-3].text.split("\n")[5][16:-1])
    prices_json = script_json['context']['dispatcher']['stores']['HistoricalPriceStore']['prices']

    prices = pd.DataFrame(prices_json)
    prices['date'] = prices['date'].apply(lambda x: datetime.date.fromtimestamp(x))
    prices.set_index('date',inplace = True)
    prices.sort_index(inplace = True)
    print(prices)

ohlc_hist('510300.SS','2018-1-1','2018-1-27', '1d')