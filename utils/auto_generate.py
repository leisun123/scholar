#coding:utf-8
"""
@file:      auto_generate
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    2017/8/1 1:27
@description:
            --
"""
import os
import sys
sys.path.append(os.path.join(os.getcwd().split('scholar')[0],'scholar'))


from scrapely import Scraper

def auto_generate(sampleurl,data,common_url):
    s = Scraper()
    s.train(sampleurl, data)
    res = (s.scrape(common_url))[0]
    for k,v in res.items():
        res[k] = v[0].replace('\n', '').strip()
    return res