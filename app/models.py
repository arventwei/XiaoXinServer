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
from app import db

class xiaoxin(Model):
    
    sn = CharField(primary_key=True)
    bind_userid = CharField()
    bind_time   = DateTimeField()
    temp = FloatField()
    humi = FloatField()
    pm25 = FloatField()
    
    class Meta:
        database = db
        
#
class user(Model):
    
    #id = PrimaryKeyField()   
    userid = CharField(primary_key=True)
    
    class Meta:
        database = db
        
#       
class xiaoxin_user(Model):
    
    id = PrimaryKeyField()   
    xiaoxin_sn = ForeignKeyField(xiaoxin, related_name='users')
    userid = CharField(primary_key=True)
    
    class Meta:
        database = db

    

