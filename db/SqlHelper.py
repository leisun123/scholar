from nameparser import HumanName

from utils.set_value import set_value

#coding:utf-8
"""
@file:      SqlHelper
@author:    IsolationWyn
@contact:   genius_wz@aliyun.com
@python:    3.5.2
@editor:    PyCharm
@create:    2017/6/29 23:12
@description:
            --
"""
import os
import sys
sys.path.append(os.path.join(os.getcwd().split('scholar')[0],'scholar'))

import datetime
from sqlalchemy import *
from sqlalchemy import exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from ScholarConfig.config import DB_CONFIG,create_ssh_tunnel
import simplejson
from db import ISqlHelper
from uuid import uuid4

from utils.logger import get_logger


BaseModel = declarative_base()

class UserGroup(BaseModel):
    __tablename__ = 'user_groups'
    __table_args__ = (
        Index('unique_user_id_group_id', 'user_id', 'group_id', unique=True),
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    group_id = Column(ForeignKey('groups.id'), nullable=False, index=True)
    group = relationship('Group')
    user = relationship('User')



class Group(BaseModel):
    __tablename__ = 'groups'

    id = Column(BigInteger, primary_key=True)
    object_id = Column(String(36), nullable=False, default='2efa4f8b-9e8b-45fe-bec4-517e4020f852')
    name = Column(String(255), nullable=False, unique=True, default='scholars')

    
class ObjectAttribute(BaseModel):
    __tablename__ = 'object_attributes'
    __table_args__ = (
        Index('object_id', 'object_id', 'name', unique=True),
    )

    id = Column(BigInteger, primary_key=True)
    object_id = Column(String(36), nullable=False)
    name = Column(String(255), nullable=False)
    value = Column(LargeBinary)
    
    def decode_value(self):
        data = simplejson.loads(bytes.decode(self.value))
        return data
    
    @staticmethod
    def update_value(sc_info, **kwargs):
        return bytes(simplejson.dumps(sc_info.update(kwargs)), encoding='utf8')
    
class Object(BaseModel):
    __tablename__ = 'objects'

    id = Column(String(36), primary_key=True, unique=True)
    parent = Column(String(36))
    type = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)


class Organization(BaseModel):
    __tablename__='organizations'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255))


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    object_id = Column(String(36), nullable=False)
    scope = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    website = Column(String(255))
    
    organization_id = Column(Integer, index=True)
    organization = Column(String(255))
    
    is_clean = Column(Boolean, default=False)
    
    password = Column(Text, nullable=False, default="bcrypt")
    reset_password_token = Column(Text)
    reset_password_sent_at = Column(DateTime)
    remember_created_at = Column(DateTime)
    sign_in_count = Column(BigInteger, nullable=False, server_default=text("'0'"))
    current_sign_in_at = Column(DateTime)
    last_sign_in_at = Column(DateTime)
    current_sign_in_ip = Column(Text)
    last_sign_in_ip = Column(Text)
    confirmation_token = Column(Text)
    confirmed_at = Column(DateTime)
    confirmation_sent_at = Column(DateTime)
    unconfirmed_email = Column(Text)
    failed_attempts = Column(Integer, nullable=False, server_default=text("'0'"))
    unlock_token = Column(Text)
    locked_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    
class Proxy(BaseModel):
    __tablename__ = 'proxys'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(VARCHAR(16), nullable=False)
    port = Column(Integer, nullable=False)
    types = Column(Integer, nullable=False)
    protocol = Column(Integer, nullable=False, default=0)
    country = Column(VARCHAR(100), nullable=False)
    area = Column(VARCHAR(100), nullable=False)
    updatetime = Column(DateTime(), default=datetime.datetime.utcnow)
    speed = Column(Numeric(5, 2), nullable=False)
    score = Column(Integer, nullable=False, default=10)

    
class SqlHelper(ISqlHelper):
    def __init__(self,logger=get_logger("TEST")):
        self.logger = logger
        if 'sqlite' in DB_CONFIG['DB_CONNECT_STRING']:
            connect_args = {'check_same_thread':False}
            self.engine = create_engine(DB_CONFIG['DB_CONNECT_STRING'],echo=False,connect_args=connect_args)
        else:
            #self.engine =create_ssh_tunnel()
            self.engine = create_engine(DB_CONFIG['DB_CONNECT_STRING'])
            DB_Session = sessionmaker(bind=self.engine)
            self.session = DB_Session()
            
    def init_db(self):
        BaseModel.metadata.create_all(bind=self.engine)
        #BaseModel.metadata.tables["organizations"].create(bind=self.engine)
        group_1 = Group(
            id = 1,
            object_id = '84193943-db89-404e-b894-02ea60ffc9b1',
            name = 'Administrators'
        )
        group_2 = Group(
            id = 2,
            object_id = 'd0d45dd3-d770-416f-b44d-cd739d2a12a0',
            name = 'Users'
        )
        group_3 = Group(
            id = 3,
            object_id = '56531a6e-f3b1-4ba5-8e88-1754a9e988e5',
            name = 'Guests'
        )
        group_4 = Group(
            id = 4,
            object_id = '4ad69298-8969-40ea-a1fd-330627a69f8c',
            name = 'Schools'
        )

        group_5 = Group(
            id = 5,
            object_id = '2efa4f8b-9e8b-45fe-bec4-517e4020f852',
            name = 'Scholars'
        )

        self.session.add(group_1)
        self.session.add(group_2)
        self.session.add(group_3)
        self.session.add(group_4)
        self.session.add(group_5)
        self.session.commit()
        

    # def drop_db(self):
    #     BaseModel.metadata.drop_all(self.engine)
    #     print("FINISH")
        
    def insert_scholar(self, **values):
        tmp_id = str(uuid4())
        tmp_create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        object = Object(
                        id = tmp_id,
                        parent = None,
                        type = "user",
                        name = "User:{}".format(tmp_id),
                        created_at = tmp_create_time
                        )
        
        user = User(
                        object_id = tmp_id,
                        scope = "",
                        name = values["name"],
                        email = values["email"],
                        password = "bcrypt",
                        reset_password_token = None,
                        reset_password_sent_at = None,
                        remember_created_at = None,
                        
                        current_sign_in_at = None,
                        last_sign_in_at = None,
                        current_sign_in_ip = None,
                        last_sign_in_ip = None,
                        confirmation_token = None,
                        confirmed_at = None,
                        confirmation_sent_at = None,
                        unconfirmed_email = None,
                        
                        unlock_token = values["avatar"],
                        locked_at = None,
                        created_at = tmp_create_time,
                        updated_at = None
        )
        
        object_attributes_profile = ObjectAttribute(
                        object_id = tmp_id,
                        name = "profile",
                        value = bytes(simplejson.dumps(values["profile"]),encoding='utf8'))


        object_attributes_password = ObjectAttribute(
                        object_id = tmp_id,
                        name = "password",
                        value = bytes(values["password"],encoding='utf8'))

        try:
            self.session.add(object)
            self.session.add(object_attributes_profile)
            self.session.add(object_attributes_password)
            self.session.add(user)
            self.session.flush()
            object_attributes_avatar = ObjectAttribute(
                        object_id = tmp_id,
                        name = "avatar",
                        value = bytes("{}.jpg".format(user.id), encoding='utf8')
                        )
            user_group = UserGroup(
                        user_id = user.id,
                        group_id = 5
                        )
            self.session.add(object_attributes_avatar)
            self.session.add(user_group)
            #download(values["avatar"],user.id,self.logger)
            self.session.commit()
            self.logger.info("{} has inserted".format(user.name))
        except exc.SQLAlchemyError as e:
            self.logger.error("{} info commit failed! Caused by {}".format(values["name"],e))
            self.session.rollback()
        finally:
            self.session.close()

    def update_scholar(self, **values):
        try:
            res = self.session.query(User).filter(User.email == values["email"])
            res.update({User.name:values["name"],
                        User.email:values["email"],
                        User.unlock_token:values["avatar"]})
            
            self.session.query(ObjectAttribute)\
                .filter(and_(ObjectAttribute.object_id == res.first().object_id, ObjectAttribute.name == "profile"))\
                    .update({ObjectAttribute.value:bytes(simplejson.dumps(values["profile"]),encoding='utf8')})
            
            self.session.commit()
            self.logger.info("{} has updated".format(res.first().name))
        except exc.SQLAlchemyError as e:
            self.logger.error("{} info updated failed! Caused by {}".format(values["name"],e))
            self.session.rollback()
        finally:
            self.session.close()
    
    def output_proxy(self):
        ipprort=self.session.query(Proxy.ip,Proxy.port).all()
        with open("../utils/1.txt","r+") as f:
             for i,j in ipprort:
                 f.writelines("{}:{}\n".format(i.replace('\'',''),j))
    
    
    
    def local_migrate(self):
        res = iter(self.session.query(User.object_id, User.id, User.organization_id, User.organization).filter(User.scope == "").all())
        try:
            while True:
                res_next = next(res)
                oj_id = res_next[0]
                user_id = res_next[1]
                og_id = res_next[2]
                og = res_next[3]
                
                
                tmp_1 = self.session.query(ObjectAttribute)\
                        .filter(and_(ObjectAttribute.object_id == oj_id, ObjectAttribute.name == "profile")).first()
                if tmp_1:
                    sc_info_byte = tmp_1.value
                else:
                    print("ObjectAttributes Missing",oj_id)
                    
                sc_info = simplejson.loads(bytes.decode(sc_info_byte))
                if "organization" not in sc_info.keys():
                    print("organization Field Missing!", oj_id)
                    sc_info["organization"] = "Unknown"
                
                if "website" not in sc_info.keys():
                    print("website Field Missing!", oj_id)
                    sc_info["website"] = "Unknown"

                try:
                    organization_object = self.session.query(Organization)\
                            .filter(or_(Organization.name == sc_info["organization"]))\
                            .first()
                except:
                    sc_info["organization"] = sc_info["organization"].encode('latin-1', 'ignore')
                    sc_info["website"] = sc_info["website"].encode('latin-1', 'ignore')
                    organization_object = self.session.query(Organization)\
                            .filter(Organization.name == sc_info["organization"])\
                            .first()
                    print("Fucking Character Error!")
                
                if organization_object is None:
                    organization = Organization(
                        name = sc_info["organization"])
                    self.session.add(organization)
                    self.session.flush()
                    organization_id = organization.id
                else:
                    organization_id = organization_object.id
                
                try:
                    self.session.query(User).filter(User.id == user_id)\
                            .update({User.organization_id: organization_id,\
                                     User.organization:  sc_info["organization"],\
                                     User.website: sc_info["website"]})
                    self.session.commit()
                    self.session.close()
                except Exception as e:
                    print(e)
                
                print("Successfully Commit One!")
        except StopIteration:
            print("----------------------------END----------------------------------")
        finally:
            res = self.session.query(User.name, User.organization ,User.website).all()
            for i in res:
                print("Name:", i[0])
                print("Organization:", i[1])
                print("Website:", i[2])
                print("--------------------------------------------")
            
    def organization_clean(self, old_id, modify_id, name=None):
        og_name = name
        if name is None:
            og_name = self.session.query(Organization).filter(Organization.id ==old_id).first().name
        self.session.query(Organization).filter(Organization.id == old_id)\
            .delete()
        self.session.query(User).filter(User.organization_id == old_id)\
            .update({"organization_id": modify_id,\
                     "organization": og_name})
        self.session.commit()
    
    
    

    def Unknow_clean(self, organization_name, email_str):
        email_match_res = self.session.query(User).filter(User.organization == "Unknown").filter(User.email.contains(email_str)).all()
        print("Finally Find {} scholars whose email end with {}".format(len(email_match_res), email_str) )
        og_tmp = self.session.query(Organization).filter(Organization.name == organization_name).first()
        if og_tmp:
            og_id = og_tmp.id
        else:
            og = Organization(
                name = organization_name
            )
            self.session.add(og)
            self.session.flush()
            og_id = og.id
        for i in email_match_res:
            self.session.query(User)\
                .filter(User.id == i.id)\
                .update({"organization_id": og_id,
                         "organization": organization_name
            })
            res = self.session.query(ObjectAttribute)\
                .filter(ObjectAttribute.name == "profile")\
                .filter(ObjectAttribute.object_id == i.object_id)\
                .first()
            sc_tmp = simplejson.loads(bytes.decode(res.value))
            sc_tmp.update({
                "organization": organization_name
            })
            print(sc_tmp)
            self.session.query(ObjectAttribute)\
                .filter(ObjectAttribute.name == "profile")\
                .filter(ObjectAttribute.object_id == i.object_id)\
                .update({ObjectAttribute.value: bytes(simplejson.dumps(sc_tmp), encoding='utf8')})
            self.session.commit()
            print("{}".format(i.name))
            print("-------------------------------------------------------------------------------------------------------------------")
            
            
        
    
    def update(self, conditions=None,value=None):
        pass
    
    def select(self, count=None,conditions=None):
        pass
    
    def close(self):
        pass
    
if __name__ == '__main__':
    sqlhelper = SqlHelper(logger=get_logger("test"))

    
    
    # count = 0
    # res = sqlhelper.session.query(Organization).all()
    # for i in res:
    #     n = sqlhelper.session.query(User).filter(User.organization_id == i.id).count()
    #     count = n + count
    # print(count)
    
    
    
    # dct = {"North Carolina State University": "ncsu.edu",
    # "Georgia Institute of Technology": "gatech.edu",
    # "University of Wisconsin-Madison": "wisc.edu",
    # "Stanford University": "stanford.edu",
    # "University of Maryland, College Park": "umd.edu",
    # "University of California,Irvine": "uci.edu",
    # "The Ohio State University": "osu.edu",
    # "University of Colorado at Boulder": "Colorado.edu",
    # "University of Illinois": "illinois.edu"}
    # for k, v in  dct.items():
    #     sqlhelper.Unknow_clean(k, v)
    #     print("clean over")
    # print("finish")
    
    # organizations = sqlhelper.session.query(Organization).all()
    # res = []
    #
    # for i in organizations:
    #     num = sqlhelper.session.query(User).filter(and_(User.organization_id == i.id,
    #                                  User.scope == '')).count()
    #
    #     if num < 40:
    #         user_object = sqlhelper.session.query(User).filter(User.organization_id == i.id).first()
    #         if user_object:
    #             user_id = user_object.id
    #             object_id = user_object.object_id
    #
    #             sqlhelper.session.query(UserGroup).filter(UserGroup.user_id == user_id).delete()
    #             sqlhelper.session.query(User).filter(User.object_id == object_id).delete()
    #             sqlhelper.session.query(Organization).filter(Organization.id == i.id).delete()
    #             sqlhelper.session.query(Object).filter(Object.id == object_id).delete()
    #             sqlhelper.session.query(ObjectAttribute).filter(ObjectAttribute.object_id == object_id).delete()
    #             sqlhelper.session.commit()
    
    # n= 0
    # res = sqlhelper.session.query(ObjectAttribute).filter(ObjectAttribute.name == 'avatar').all()
    # for i in res:
    #
    #     user_info = (bytes.decode(i.value))
    #     if '.jpg' not in user_info:
    #         n = n + 1
    #         tmp = simplejson.loads(user_info)
    #         print(tmp["website"], i.id)
    # print(n)

    # tmp = iter(sqlhelper.session.query(ObjectAttribute).filter(ObjectAttribute.name == "profile").all())
    # try:
    #     while True:
    #         iter_obj = next(tmp)
    #         sc_info = iter_obj.decode_value()
    #         if "lastName" not in sc_info:
    #             if "name" in sc_info:
    #                 if isinstance(sc_info["name"], list):
    #                     sc_info["firstName"] = HumanName(sc_info["name"][0]).first
    #                     sc_info["lastName"] = HumanName(sc_info["name"][0]).last
    #                 else:
    #                     sc_info["firstName"] = HumanName(sc_info["name"]).first
    #                     sc_info["lastName"] = HumanName(sc_info["name"]).last
    #             if "firstName" in sc_info:
    #                 sc_info["firstName"] = HumanName(sc_info["firstName"]).first
    #                 sc_info["lastName"] = HumanName(sc_info["firstName"]).last
    #             else:
    #                 sqlhelper.session.query(ObjectAttribute).filter(ObjectAttribute.id == iter_obj.id).delete()
    #                 sc_info["lastName"] = "error"
    #
    #
    #
    #         if sc_info['lastName'] is None or sc_info['lastName'] == "":
    #             if sc_info["firstName"]:
    #                 iter_obj.value =  ObjectAttribute.update_value(sc_info,
    #                                       firstName = HumanName(sc_info["firstName"]).first,
    #                                       lastName = HumanName(sc_info["lastName"]).last)
    #                 if sqlhelper.session.query(User)\
    #                         .filter(User.object_id == iter_obj.object_id).first():
    #                     sqlhelper.session.query(User)\
    #                         .filter(User.object_id == iter_obj.object_id)\
    #                         .update({"name": sc_info["firstName"] + " " + sc_info["lastName"]
    #                         })
    #                     print("firstName", sc_info["firstName"])
    #                     print("lastName", sc_info["lastName"])
    #                     print("Name", sqlhelper.session.query(User).filter(User.object_id == iter_obj.object_id).first().name)
    #                     print("firstName",sqlhelper.session.query(ObjectAttribute).filter(ObjectAttribute.id == iter_obj.id).first().id)
    #                     #print("lastName",sqlhelper.session.query(ObjectAttribute).filter(ObjectAttribute.id == iter_obj.id).first().decode_value()["lastName"])
    #                     print("-------------------------------------------------------------------")
    #
    #
    # except StopIteration as e:
    #     print(e)
    # finally:
    #     print("End")
    
    
    major_count = 0
    avatar_count = 0
    website_count = 0
    
    res = iter(sqlhelper.session.query(ObjectAttribute)\
               .filter(ObjectAttribute.name == 'profile').all())
    while True:
        data = next(res).decode_value()
        if data["major"] == None or data["major"] == "":
            major_count = major_count + 1
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    