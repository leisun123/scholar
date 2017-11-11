#coding:utf-8
"""
@file:      url_cache
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    2017/11/12 0:11
@description:
            --
"""
import re

import redis

from db.SqlHelper import *

redis_obj = redis.Redis(host='localhost', port=6379, db=1)

def run():
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