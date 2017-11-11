#coding:utf-8
"""
@file:      script.py
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    2017/10/8 16:17
@description:
            --
"""
rootdir = "C:/Users/tonylu/Desktop/111"
from db.SqlHelper import *

# for img in os.listdir(rootdir):
#     initial_name = img
#     src = os.path.abspath(os.path.join(rootdir, img))
#     print(src)
#     sqlhelper = SqlHelper(logger=get_logger("test"))
#     oj_id = sqlhelper.session.query(ObjectAttribute).filter(ObjectAttribute.id == initial_name.split('.')[0]).first().object_id
#     user_id = sqlhelper.session.query(User).filter(User.object_id == oj_id).first().id
#     print(user_id)
#     try:
#         os.rename(src, os.path.abspath(os.path.join(rootdir, '{}_.jpg'.format(user_id))))
#     except Exception as e:
#         print(e)
for img in os.listdir(rootdir):
    os.rename(os.path.abspath(os.path.join(rootdir, img)), os.path.abspath(os.path.join(rootdir, img.replace('_', ''))))