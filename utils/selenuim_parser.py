#coding:utf-8
"""
@file:      webdriver
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    2017/6/30 2:36
@description:
            --
"""
import os
import sys
sys.path.append(os.path.join(os.getcwd().split('scholar')[0],'scholar'))


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

def SelenuimParser(proxy_manager, user_agent, use_proxy):
    
    driver_option = webdriver.ChromeOptions()
    if use_proxy:
        driver_option.add_argument('--proxy-server={}'.format(use_proxy))
    driver_option.add_argument('--user-agent={}'.format(user_agent))
    driver = webdriver.Chrome()
    driver
    return driver


if __name__ == '__main__':
   driver = webdriver.Chrome()
   driver.get("http://eng.auburn.edu/aero/faculty/")
   print(driver.session_id)
   # html_source = (driver.page_source)
   # print(html_source)
   # from utils.connection import *
   # email = extract("//p[contains(text(),'@')]/./text()", html_source)
   # print(email)
   # import re
   # regex = r"([\w\.\-]+@[\w\.\-]+)"
   #
   #
   # print("-------------------------------------------")
   # email = re.search(regex, html_source).group()
   # print(email)
   