#coding:utf-8
"""
@file:      graphics_stanford_parser
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    2017/7/20 15:49
@description:
            --
"""
from lxml import etree

from BaseClass.ThesisClass import ThesisInfo
from ErrorHandle.parse_error import except_pass
from db.SqlHelper import SqlHelper
from utils.connection import extract
from ScholarConfig.che_utexas_rule  import RULES
from nameparser import HumanName
from TaskFeed.graphics_stanford_task import GraphicsStanfordTask
PS_ERROR = lambda func:except_pass(func,ModelName = 'graphics_stanford')

class GraphicsStanfordClass(ThesisInfo):
    def __init__(self,sec):
        """
        :param sec: item url
        """
        self.sec = sec
        super(GraphicsStanfordClass, self).__init__()
        self.generate_all_method()
        parm=self.set_value()
        sqlhelper=SqlHelper(GraphicsStanfordTask.logger)
        sqlhelper.insert_scholar_thesis(**parm)
    
    def _generate_avatar(self):
        self.avatar = extract(RULES["avatar"],self.sec)
    def _generate_firstName(self):
        tmp = extract(RULES["name"],self.sec)
        self.firstName = HumanName(tmp).first
    def _generate_lastName(self):
        tmp = extract(RULES["name"],self.sec)
        self.lastName = HumanName(tmp).last
    def _generate_organization(self):
        self.organization = "The University of Texas at Austin"
    def _generate_major(self):
        self.major = "McKetta Department of Chemical Engineering"
    def _generate_title(self):
        self.title = extract(RULES["title"],self.sec)
    def _generate_birth(self):
        pass
    def _generate_country(self):
        pass
    def _generate_state(self):
        pass
    def _generate_maincity(self):
        if len(self.city) != 0:
            self.maincity = self.city[0]
            
    def _generate_phone(self):
        self.phone = extract(RULES["phone"],self.sec)
        
    def _generate_email(self):
        tmp = extract(RULES["email"],self.sec)
        if tmp is not None:
            self.email = tmp.xpath('string(.)')
    def _generate_website(self):
        pass
    def _generate_cooperation(self):
        tmp = extract(RULES["cooperation"],self.sec)
        if tmp is not None:
            self.cooperation = tmp.strip().split(',')
    def _generate_bio(self):
        tmp = extract(RULES["bio"],self.sec)
        if tmp is not None:
            self.bio = tmp.xpath('string(.)')
    def _generate_keywords(self):
        self.keywords = extract(RULES["keywords"],self.sec,multi=True)
        
    def _generate_city(self):
        pass
    def _generate_time(self):
        pass
    def _generate_keywordKeys(self):
        self.keywordKeys = [i for i in range(1,len(self.keywords)+1)]
    def _generate_cityKeys(self):
        self.cityKeys = [i for i in range(1,len(self.city)+1)]
    def _generate_timeKeys(self):
        self.timeKeys = [i for i in range(1,len(self.timeKeys)+1)]

if __name__ == '__main__':
    from utils.connection import fetch
    html= fetch("https://profiles.stanford.edu/abbas-el-gamal?tab=bio")
    a=extract(RULES["avatar"],html)
    print(a)