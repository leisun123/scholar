# coding:utf-8
"""
@file:      page_screenshot
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    2017/11/10 21:31
@description:
            --
"""
# -*- coding: utf-8 -*-
from queue import Queue
import os
import sys
sys.path.append(os.path.join(os.getcwd().split('scholar')[0],'scholar'))
import time
from selenium import webdriver
from db.SqlHelper import *
import re
import redis
import threading

redis_obj = redis.Redis(host='localhost', port=6379, db=5)


sqlhelper = SqlHelper(logger=get_logger("test"))
sc_info_list = iter(sqlhelper.session.query(ObjectAttribute).filter(ObjectAttribute.name == "profile").all())
try:
  while True:
    iter_tmp = next(sc_info_list)
    sc_info = iter_tmp.decode_value()

    user_obj = sqlhelper.session.query(User).filter(User.object_id == iter_tmp.object_id).first()
    user_id = user_obj.id if user_obj else None
    if "website" in sc_info.keys():
      sc_website = sc_info["website"]
    else:
      sc_website = None

    if user_id and sc_website:
      if re.match(r'^https?:/{2}\w.+$', sc_website):
        print(sc_website)
        redis_obj.set(user_id, sc_website)
except StopIteration as e:
  print(e)
finally:
  redis_obj.save()

driver = webdriver.PhantomJS("D:\Python33\Scripts\phantomjs.exe", service_args=['--disk-cache=yes', '--ignore-ssl-errors=true'])
def screenshot(id, url):
    try:
        print(str(url.decode("utf-8")))
        driver.implicitly_wait(10)
        driver.get(str(url.decode("utf-8")))
        driver.save_screenshot('{}.jpg'.format(int(id)))
    except Exception as e:
        print(e)
    
    
for i in redis_obj.scan_iter():
    screenshot(i.decode("utf-8"), redis_obj.get(i))
    
    
    
# class phantomjs_screenshot():
#     service_args = ['--disk-cache=yes', '--ignore-ssl-errors=true']
#     sdk_path = "D:\Python33\Scripts\phantomjs.exe"
#     max_thread = 10
#     time_out = 10
#     sleep_time = 0.00001
#     th = []
#
#     def __init__(self):
#         self.phantomjs_queue = Queue()
#         self.url_list = redis_obj.scan_iter()
#         self.init_phantomjs_driver_pool()
#
#
#     def screenshot(self, url):
#         driver = self.phantomjs_queue.get()
#         try:
#             driver.get(url)
#         except:
#             print("Phantomjs Open url Error")
#
#         print(driver.current_url)
#         self.phantomjs_queue.put(driver)
#
#     def init_phantomjs_driver_pool(self):
#         def open_threading():
#             driver = webdriver.PhantomJS(phantomjs_screenshot.sdk_path, service_args=phantomjs_screenshot.service_args)
#             driver.implicitly_wait(phantomjs_screenshot.time_out)
#             phantomjs_screenshot.phantomjs_queue.put(driver)
#
#         for i in range(self.max_thread):
#             t = threading.Thread(target=open_threading)
#             self.th.append(t)
#         for i in self.th:
#             i.start()
#             time.sleep(self.sleep_time)
#         for i in self.th:
#             i.join()
#
#     def run(self):
#         for i in redis_obj.scan_iter():
#
#
# if __name__ == '__main__':
#     cur = phantomjs_screenshot()
#     cur.open_phantomjs()
#     for i in redis_obj.scan_iter():
#         t =
    
