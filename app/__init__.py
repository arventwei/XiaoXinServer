#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

from flask import Flask
from flask import g
from flask import redirect
from flask import request
from flask import session
from flask import url_for, abort, render_template, flash
from functools import wraps
from hashlib import md5
from peewee import *
from log import info,debug,log

# config - aside from our database, the rest is for use by Flask
DATABASE = 'xiaoxin.db'
DEBUG = True
SECRET_KEY = 'hin6bab8ge25*r=x&amp;+5$0kn=-#log$pt^#@vrqjld!^2ci@g*b'

# create a flask application - this ``app`` object will be used to handle
# inbound requests, routing them to the proper 'view' functions, etc
app = Flask(__name__)
app.config.from_object(__name__)

# create a peewee database instance -- our models will use this database to
# persist information
db = SqliteDatabase(DATABASE)


class Xiaoxin(Model):
    
    sn = CharField(unique=True)
    bind_userid = CharField(default="")
    bind_time   = DateTimeField(default=datetime.datetime.now())
    temp = FloatField(default=20)
    humi = FloatField(default=20)
    pm25 = FloatField(default=20)
    
    class Meta:
        database = db
        
#
class User(Model):
    
    #id = PrimaryKeyField()   
    userid = CharField(unique=True)
    name=CharField()
    age=IntegerField()
    gender=IntegerField()
    
    
    class Meta:
        database = db
        
#       
class XiaoxinUser(Model):
    
    #id = PrimaryKeyField()   
    
    user = ForeignKeyField(User, related_name='xiaoxins')
    xiaoxin = ForeignKeyField(Xiaoxin, related_name='users')
    
    
    class Meta:
        database = db



# request handlers -- these two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.  peewee will do
# this for us, but its generally a good idea to be explicit.
@app.before_request
def before_request():
    g.db = db
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response
    
# simple utility function to create tables
def create_tables():
    db.connect()
    Xiaoxin.create_table(True)
    User.create_table(True)
    XiaoxinUser.create_table(True)
    
@app.route('/')
def route_index():
    return 'Index Page<br>'+print_xiaoxin_help()

@app.route('/install')
def route_install():
    create_tables()
    return "install succeed"



def print_xiaoxin_help():
    ret =  """
    <br>
    小新接口说明：<br>
    1.请使用POST方式提交数据，格式如下<br>
    POST http://211.103.161.120:9999/xiaoxin/config HTTP/1.1<br>
    Content-Type: application/x-www-form-urlencoded;charset=utf-8<br>
    sn=123456123&userid=sina_123456<br>
    注意:数据提交不是json格式了，而是采用简单的form表单形式，主要是我们的数据比较简单，JSON比较复杂。<br>
    form格式如下<br>
    name=value&name2=value2<br>
    每个key和value之间用=连接，key-value之间用&连接。<br>
    <br>
    2.程序会返回Ok和Fail两种类型值<br>
    <br>
    接口如下：<br>
    3.1.小新配置接口  /xiaoxin/config<br>
       1 当小新设置按钮按下时，小新等待手机的WIFI配置信息，<br>
       2 当小新配置完毕后，保存sn和userid.连接WIFI网络，并把这两个值发给服务器。<br>
       3 发送格式如下 sn=123456123&userid=sina_123456 ,注意 sn和userid都是小写<br>
       4 测试例子：<br>
       curl --data "sn=123456123&userid=sina_123456" http://211.103.161.120:9999/xiaoxin/config<br>
       <br>

    3.2.小新提交数据接口 /xiaoxin/upload<br>
       1. 小新启动后，检测已经配置过,(sn不为空)<br>
       2. 尝试连接WIFI网络。如果连接不上，尝试连接固定的手机WIFI入口。<br>
       3. 手机的WIFI入口固定为 name:xiaoxin_mobile   password:1234$#@!xiaoxin<br>
       4.连接到网络后，发送信息给服务器，主要是，温度(temp),湿度(humi),pm25(pm25)<br>
       5.测试例子：<br>
       curl --data "sn=123456123&temp=20.5&humi=30&pm25=100" http://211.103.161.120:9999/xiaoxin/upload<br>
    """;
    
    return ret;
    
def getformValue(form,name):
    if name not in form.keys():
        debug(name+" is null");
        raise Exception(name+" is null")
        debug("s");
    return form[name]
@app.route('/xiaoxin/<action>', methods=['GET', 'POST'])
def route_xiaoxin(action):
    
    #return "Failed"
    if request.method == "GET":
        return print_xiaoxin_help();
   
    info(request.form)
    
    if action == "config":
        return xiaoxin_config(request.form)
    elif action=="upload":
        return xiaoxin_upload(request.form)
    
    
   

def xiaoxin_config(form):
    try:   
        _sn = getformValue(form,"sn")
        _userid =getformValue(form,"userid")
        
        xiaoxin = Xiaoxin.get_or_create(sn=_sn)
        
        xiaoxin.bind_userid=_userid
        xiaoxin.bind_time = datetime.datetime.now()
        xiaoxin.save()
    except Exception as e:
        debug(e)
        return "Fail"
    return "Ok"


def xiaoxin_upload(form):
    try:
        _sn = getformValue(form,"sn")
        _temp =getformValue(form,"temp")
        _humi =getformValue(form,"humi")
        _pm25 =getformValue(form,"pm25")
        
    
        xiaoxin = Xiaoxin.get_or_create(sn = _sn)
  
        xiaoxin.temp = _temp
        xiaoxin.humi = _humi
        xiaoxin.pm25 = _pm25
        xiaoxin.save()
    except Exception as e:
        debug(e)
        return "Fail"

    return "Ok"
    
    