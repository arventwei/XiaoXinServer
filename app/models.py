# -*- coding: utf-8 -*-
'''
Created on 2014-3-10

@author: will
'''

#todo
#http://peewee.readthedocs.org/en/latest/peewee/api.html#Model
#http://peewee.readthedocs.org/en/latest/peewee/example.html#example-app


import time
from log import info,debug,log
from peewee import *
from app import database

class xiaoxin(Model):
    
    id = CharField()
    
    class Meta:
        database = database
        
class xiaoxin(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)                                                   
    sn = Column(String(20), unique=True)
    bind_userid = Column(String(20))
    bind_time = Column(Integer)
    
    temp = Column(Float)
    humi = Column(Float)
    pm25 = Column(Float)
                                                              
    def __init__(self, sn=None, bind_userid=None):
        self.sn = sn
        self.bind_userid = bind_userid
                                                              
    def __repr__(self):
        return '%s (%r, %r)' % (self.__class__.__name__, self.sn, self.bind_userid)


class user(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)   
    userid = Column(String(20), unique=True)
    
    def __init__(self,userid):
        self.userid=userid
        
    def __repr__(self):
        return '%s (%r)' % (self.__class__.__name__, self.userid)
    

