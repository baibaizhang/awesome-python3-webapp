#!/usr/bin/env python3
#coding:utf-8  
''''' 
@author: steve 
获取筹码分布数据
'''  
 
import re,time,random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import pyautogui
from operator import itemgetter
from itertools import groupby

class CMFBData(object):
    def __init__(self, load_parameter='silent'):
        # print(self.__class__.__name__+" __init__")
        # 给浏览器设置属性
        option = webdriver.ChromeOptions()
        # 隐藏警告语‘Chrome正在受到自动软件的控制’
        option.add_argument('disable-infobars')
        # 设置隐藏还是前台运行,默认隐藏
        if load_parameter == 'silent':
            option.add_argument("headless")
        # 产生随机user-agent
        option.add_argument(UserAgent().random)
        self.browser = webdriver.Chrome(options=option)

        if not (load_parameter == 'silent'):
            #最大化浏览器
            self.browser.maximize_window()
            

        self.timeoutCodeList = []
        self.retrytime = 3
        

    def __del__(self):
        # 关闭浏览器
        self.browser.quit()
        # print(self.__class__.__name__+" __del__")

    # 解析网页获取筹码分布数据并返回数据
    def _get_cmfb_data(self):
        COLUMN_LIST = ('日期','获利比例','亏损比例','平均成本','90%成本','90成本集中度','70%成本','70成本集中度')
        count = len(COLUMN_LIST)
        data = {}
        index = 0
        # 解析网页
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        for span in soup.find(class_="__emchatrs3_cmfb").find_all('span'):
            if index >= count:
                break
            if index == 0:
                date = span.contents[0]
            data[COLUMN_LIST[index]] = span.contents[0]
            index = index + 1

        # print(data)
        return data
        

    def _get_url(self, code):
        codelist = {'60': 'sh', '00':'sz', '30':'sz'}
        for item in codelist:
            if code.startswith(item):
                return "http://quote.eastmoney.com/concept/" + codelist[item] + code + ".html"

    # 打开并加载网页，等待完成
    def _load_web(self, url):
        # 这里经常出现加载超的异常，后面需要处理一下：捕获异常后，刷新浏览器
        retry_time = 3
        while True:
            if retry_time == 0:
                return False
            try:
                browser = self.browser
                browser.get(url)
                # 找到筹码分布的按钮---通过xpath
                btn_cmfb_xpath = "//a[text()='筹码分布']"
                # 等待响应完成
                wait = WebDriverWait(browser, 10)
                wait.until(EC.presence_of_element_located((By.XPATH, btn_cmfb_xpath)))
                # 查找目标按钮
                btn_cmfb = browser.find_element_by_xpath(btn_cmfb_xpath)
                # 找到按钮后单击
                btn_cmfb.click()

                # 等待筹码分布的元素显示出来，不然解析数据的时候抓取不到相关数据
                wait = WebDriverWait(browser, 10)
                # wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='__emchatrs3_cmfb']" )))
                # wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='__emchatrs3_cmfb']" )))
                wait.until(EC.text_to_be_present_in_element((By.XPATH,"//div[@class='__emchatrs3_cmfb']"),u'集中度'))
                return True
            except TimeoutException:
                retry_time = retry_time - 1
                continue

    def get_data_current(self,code):
        # data_list = []
        data={}

        url = self._get_url(code)
        # 如果网页加载失败,直接返回
        if not self._load_web(url):
            print("网页加载失败: " + url)
            return data
        
        data = self._get_cmfb_data()
        return data
        # data_list.append(data)

        # print(data_list)
        # return data_list

    def get_data_history(self,code):
        data_list = []

        url = self._get_url(code)
        # 如果网页加载失败,直接返回
        if not self._load_web(url):
            print("网页加载失败: " + url)
            return data_list
        
        browser = self.browser
        # 移动滚动条定位到某个元素，使这个元素在可见区域，一般在最顶上
        target = browser.find_element_by_xpath("//div[@class='kr-box']")
        # target = browser.find_element_by_xpath(btn_cmfb_xpath)
        browser.execute_script("arguments[0].scrollIntoView();", target)

        time.sleep(2)
        # 移动到某个起始位置
        START_X = 0
        START_Y = 0 
        END_X = 0
        MOVE_X = 0
        screenWidth,screenHeight = pyautogui.size()
        print("screenWidth : " + str(screenWidth))
        if screenWidth == 1366 :
            START_X = 350
            END_X = 996
            START_Y = 485
            MOVE_X = 8
        elif screenWidth == 1920:
            START_X = 544    
            END_X = 1350
            START_Y = 666
            MOVE_X = 10
        else:
            print("不能匹配到屏幕尺寸，请增加")
            return
        currentX= START_X
        currentY= START_Y

        pyautogui.moveTo(START_X, START_Y)
        time.sleep(2)

        while currentX < END_X:
            data = self._get_cmfb_data()
            data_list.append(data)

            # #  鼠标向右移动x像素
            currentX = currentX + MOVE_X
            pyautogui.moveTo(currentX, currentY)
            # 等待筹码分布的元素显示出来，不然解析数据的时候抓取不到相关数据
            wait = WebDriverWait(browser, 10)
            # wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='__emchatrs3_cmfb']" )))
            # wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='__emchatrs3_cmfb']" )))
            wait.until(EC.text_to_be_present_in_element((By.XPATH,"//div[@class='__emchatrs3_cmfb']"),u'集中度'))

        # data_list 需要去重和排序
        print(data_list)
        print(len(data_list))
        data_list = self._distinct(data_list, '日期')
        print(len(data_list))
        print(data_list)
        return data_list

    # 含dict的list排序并去重
    def _distinct(self, items,key, reverse=False):
        key = itemgetter(key)
        items = sorted(items, key=key, reverse=reverse)
        return [next(v) for _, v in groupby(items, key=key)]
 

def main():
    # http://quote.eastmoney.com/concept/sz000002.html
    # test = CMBFData()
    # test.get_data_current('000002')

    # 抓取历史数据必须打开浏览器到前台
    test = CMBFData('show_browser')
    test.get_data_history('000002')
    # test.getData('000002')
    # test.getData('601318')
    # test.getData('300002')
 
 
 
if __name__ == '__main__':
    main()
