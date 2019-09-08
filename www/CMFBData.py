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

class CMBFData(object):
    def __init__(self):
        print(self.__class__.__name__+" __init__")
        # # 给浏览器设置属性
        # option = webdriver.ChromeOptions()
        # # 设置默认隐藏，后台运行
        # option.add_argument("headless")
        # # 产生随机user-agent
        # option.add_argument(UserAgent().random)
        # self.browser = webdriver.Chrome(options=option)

        # 显示打开chrome浏览器（需提前安装好chromedriver）
        self.browser = webdriver.Chrome()
        #最大化浏览器
        self.browser.maximize_window()

        self.timeoutCodeList = []
        self.retrytime = 3
        

    def __del__(self):
        # 关闭浏览器
        self.browser.quit()
        print(self.__class__.__name__+" __del__")


    def getDataFromWeb(self, url):
        cmfb_data = {}

        # 这里经常出现加载超的异常，后面需要处理一下：捕获异常后，刷新浏览器
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

        
        # 移动滚动条定位到某个元素，使这个元素在可见区域，一般在最顶上
        target = browser.find_element_by_xpath("//div[@class='kr-box']")
        # target = browser.find_element_by_xpath(btn_cmfb_xpath)
        browser.execute_script("arguments[0].scrollIntoView();", target)

        time.sleep(2)
        # 移动到某个起始位置
        START_X = 544
        END_X = 1350
        START_Y = 666
        MOVE_X = 10
        currentX= START_X
        currentY= START_Y

        pyautogui.moveTo(START_X, START_Y)
        time.sleep(2)

        COLUMN_LIST = ('日期','获利比例','亏损比例','平均成本','90%成本','90成本集中度','70%成本','70成本集中度')
        count = len(COLUMN_LIST)
        while currentX < END_X:
            data = {}
            index = 0
            # 解析网页
            soup = BeautifulSoup(browser.page_source, 'lxml')
            for span in soup.find(class_="__emchatrs3_cmfb").find_all('span'):
                if index >= count:
                    break
                if index == 0:
                    date = span.contents[0]
                data[COLUMN_LIST[index]] = span.contents[0]
                index = index + 1

            print(data)
            cmfb_data[date] = data

            # #  鼠标向右移动x像素
            currentX = currentX + MOVE_X
            pyautogui.moveTo(currentX, currentY)
            # time.sleep(1)
            # 等待筹码分布的元素显示出来，不然解析数据的时候抓取不到相关数据
            wait = WebDriverWait(browser, 10)
            # wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='__emchatrs3_cmfb']" )))
            # wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='__emchatrs3_cmfb']" )))
            wait.until(EC.text_to_be_present_in_element((By.XPATH,"//div[@class='__emchatrs3_cmfb']"),u'集中度'))
            

            # tag = soup.find(class_="__emchatrs3_cmfb")
            # #print(tag.div.label.string)
            # m_label = tag.findAll('label')
            # m_span = tag.findAll('span')
            

            # # 日期
            # cmfb_data[m_label[0].contents[0]] = m_span[0].contents[0]
            # # print(m_label[0].contents[0] + " " + m_span[0].contents[0])
            # # 获利比例
            # cmfb_data[m_label[1].contents[0]] = m_span[1].contents[0]
            # # print(m_label[1].contents[0] + " " + m_span[1].contents[0])
            # # 平均成本
            # cmfb_data[m_label[3].contents[0]] = m_span[3].contents[0]
            # # print(m_label[3].contents[0] + " " + m_span[3].contents[0])
            # # 90%成本
            # cmfb_data[m_label[4].contents[0]] = m_span[4].contents[0]
            # # print(m_label[4].contents[0] + " " + m_span[4].contents[0])
            # # 90集中度
            # cmfb_data['90'+m_label[5].contents[0]] = m_span[5].contents[0]
            # # print(m_label[5].contents[0] + " " + m_span[5].contents[0])
            # # 70%成本
            # cmfb_data[m_label[6].contents[0]] = m_span[6].contents[0]
            # # print(m_label[6].contents[0] + " " + m_span[6].contents[0])
            # # 70集中度
            # cmfb_data['70'+m_label[7].contents[0]] = m_span[7].contents[0]
            # # print(m_label[7].contents[0] + " " + m_span[7].contents[0])

        print(len(cmfb_data))
        print(cmfb_data)
        return cmfb_data


    def getUrl(self, code):
        codelist = {'60': 'sh', '00':'sz', '30':'sz'}
        for item in codelist:
            if code.startswith(item):
                return "http://quote.eastmoney.com/concept/" + codelist[item] + code + ".html"

    def getDataInternel(self, code):
        try:
            time.sleep(random.randint(0,3)+random.random()) #随机延时?.?s  以防封IP
            url = self.getUrl(code)
            data = self.getDataFromWeb(url)
            # code
            print("股票代码: " + code)
            # print(data)
        except TimeoutException as e:
            self.retrytime = self.retrytime - 1
            print(code + " retrytime left " + str(self.retrytime))
            if self.retrytime > 0 : 
                self.getDataInternel(code)
            else:
                self.timeoutCodeList.append(code)
        finally:
            pass
    
    def getData(self, code, retrytime=3):
        self.retrytime = retrytime
        self.getDataInternel(code)   



def main():
    test = CMBFData()
    test.getData('000002')
    # test.getData('601318')
    # test.getData('300002')
 
 
 
if __name__ == '__main__':
    main()