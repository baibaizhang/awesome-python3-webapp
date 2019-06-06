#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'steve'

'''

'''

from yahoo_finance import Share
from pprint import pprint

def hist(tickCode, start_date, end_date):
    stock = Share(tickCode)
    prices = stock.get_historical(start_date, end_date)
    print(prices)
    pprint(prices)


hist('YHOO','2018-1-1','2018-1-27')