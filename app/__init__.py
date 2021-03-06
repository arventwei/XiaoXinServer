#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import time

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
from config import localip
import uuid

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
    name=CharField(default="小新")
    bind_userid = CharField(default="")
    bind_time   = DateTimeField(default=datetime.datetime.now())
    temp = FloatField(default=20)
    humi = FloatField(default=20)
    pm25 = FloatField(default=20)
    form = FloatField(default=1)
    last_upload_time   = FloatField(default=time.time())
    
    #set by mobile, get by xiaoxin
    switch = IntegerField(default=1)
    speed  = IntegerField(default=1)
    class Meta:
        database = db
        
#
class User(Model):
    
    #id = PrimaryKeyField()   
    userid = CharField(unique=True)
    name=CharField(default="")
    age=IntegerField(default=0)
    gender=IntegerField(default=0)
    
    
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
    Xiaoxin.create_table()
    User.create_table()
    XiaoxinUser.create_table()
    
@app.route('/')
def route_index():
    return print_xiaoxin_help()+print_mobile_help()

@app.route('/install')
def route_install():
    create_tables()
    return "install succeed"



def print_xiaoxin_help():
    ret =  """
    <br>
    小新接口说明：<br>
    1.请使用POST方式提交数据，格式如下<br>
    POST http://"""+localip+""":9999/xiaoxin/config HTTP/1.1<br>
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
       3 发送格式如下 sn=111&userid=sina_123456 ,注意 sn和userid都是小写<br>
       4 测试例子：<br>
       curl --data "sn=111&userid=123" http://"""+localip+""":9999/xiaoxin/config<br>
       <br>

    3.2.小新提交数据接口 /xiaoxin/upload<br>
       1. 小新启动后，检测已经配置过,(sn不为空)<br>
       2. 尝试连接WIFI网络。如果连接不上，尝试连接固定的手机WIFI入口。<br>
       3. 手机的WIFI入口固定为 name:xiaoxin   password:1234567890<br>
       4.连接到网络后，发送信息给服务器，主要是，温度(temp),湿度(humi),pm25(pm25),甲醛(form)<br>
       5.测试例子：<br>
       curl --data "sn=111&temp=20.5&humi=30&pm25=100&form=33" http://"""+localip+""":9999/xiaoxin/upload<br>
       <br>
    3.3.小新查询状态接口 /xiaoxin/status<br>
       1. 返回是否开关，和风速信息 格式如: switch=0&speed=1<br>
       2 0表示关，1表示开<br>
       5.测试例子：<br>
       curl --data "sn=111" http://"""+localip+""":9999/xiaoxin/status<br>
    """;
    
    return ret;
def print_mobile_help():
    ret =  """
    <br>
    APP接口说明：<br>
    <br>
    接口如下：<br>


    3.1.手机用户登录 /mobile/login<br>
       1. App启动后,发送userid和用户信息给服务器<br>
       2. 服务器接受后，保存信息返回Fail或Ok<br>
       3.测试例子：<br>
       curl --data "userid=123&age=20.5&gender=1&name=xxx" http://"""+localip+""":9999/mobile/login<br><br>
    3.1.用户绑定小新 /mobile/bind<br>
       1. 发送userid和sn给服务器<br>
       2. 服务器接受后，保存信息返回Fail或Ok<br>
       3.测试例子：<br>
       curl --data "userid=123&sn=111" http://"""+localip+""":9999/mobile/bind<br><br>
    3.2.用户解除绑定小新 /mobile/unbind<br>
       1. 发送userid和sn给服务器<br>
       2. 服务器接受后，返回Fail或Ok<br>
       3.测试例子：<br>
       curl --data "userid=123&sn=111" http://"""+localip+""":9999/mobile/unbind<br><br>
    3.2.用户查询小新列表 /mobile/query_bindlist<br>
       1. 发送userid给服务器<br>
       2. 服务器接受后，返回Fail或列表信息<br>
       3.测试例子：<br>
       curl --data "userid=123" http://"""+localip+""":9999/mobile/query_bindlist<br>  <br>
    3.3.获取小新数据 /mobile/getxiaoxin<br>
       1. 发送sn信息给服务器<br>
       2. 服务器接受后，回Fail或小新信息<br>
       3.测试例子：<br>
       curl --data "sn=111" http://"""+localip+""":9999/mobile/getxiaoxin<br><br>
    3.4.设置小新开关 /mobile/setxiaoxin_switch<br>
       1. 发送sn信息给服务器<br>
       2. 服务器接受后，回Fail或小新信息<br>
       3.测试例子：<br>
       curl --data "sn=111&switch=1" http://"""+localip+""":9999/mobile/setxiaoxin_switch<br><br>
    3.5.设置小新速度 /mobile/setxiaoxin_speed<br>
       1. 发送sn信息给服务器<br>
       2. 服务器接受后，回Fail或小新信息<br>
       3.测试例子：<br>
       curl --data "sn=111&speed=1" http://"""+localip+""":9999/mobile/setxiaoxin_speed<br><br>
 3.6.设置小新名字 /mobile/setxiaoxin_name<br>
       1. 发送sn信息给服务器<br>
       2. 服务器接受后，回Fail或小新信息<br>
       3.测试例子：<br>
       curl --data "sn=111&name=xxx" http://"""+localip+""":9999/mobile/setxiaoxin_speed<br><br>
    """;
    
    return ret;
def getformValue(form,name):
    if name not in form.keys():
        debug(name+" is null");
        raise Exception(name+" is null")
    if len(form[name])==0:
    	return "0";
     
    return form[name]
@app.route('/xiaoxin/<action>', methods=['GET', 'POST'])
def route_xiaoxin(action):
    
    #return "Failed"
    if request.method == "GET":
        return print_mobile_help();
   
    info(action+":"+str(request.form))
    
    if action == "config":
        return xiaoxin_config(request.form)
    elif action=="upload":
        return xiaoxin_upload(request.form)
    elif action=="status":
        return xiaoxin_status(request.form)
    
    return "Fail"
    
   

def xiaoxin_config(form):
    try:   
        _sn = getformValue(form,"sn")
        _userid =getformValue(form,"userid")
        
        xiaoxin = Xiaoxin.get_or_create(sn=_sn)
        
        xiaoxin.bind_userid=_userid
        xiaoxin.bind_time = datetime.datetime.now()
        xiaoxin.save()
        return "Ok"
    except Exception as e:
        debug(e)
    return "Fail"
    
def xiaoxin_status(form):
    try:   
        _sn = getformValue(form,"sn")
        
        xiaoxin = Xiaoxin.get(Xiaoxin.sn==_sn)
        cur_switch = xiaoxin.switch
        #xiaoxin.switch=True
        #xiaoxin.save()
        return "switch=%i&speed=%d" % (cur_switch,xiaoxin.speed)
    except Exception as e:
        debug(e)
    return "Fail"

def xiaoxin_upload(form):
    try:
        _sn = getformValue(form,"sn")
        _temp =getformValue(form,"temp")
        _humi =getformValue(form,"humi")
        _pm25 =getformValue(form,"pm25")
        _form =getformValue(form,"form")
        
    
        xiaoxin = Xiaoxin.get_or_create(sn = _sn)
  
        xiaoxin.temp = _temp
        xiaoxin.humi = _humi
        xiaoxin.pm25 = _pm25
        xiaoxin.form = _form
        xiaoxin.last_upload_time = time.time()
        xiaoxin.save()
        return "Ok"
    except Exception as e:
        debug(e)
        
    return "Fail"
    

def mobile_login(form):
    try:
       
        _userid =getformValue(form,"userid")
        user = User.get_or_create(userid=_userid)
        if  user.xiaoxins.count() ==0:
            xx = Xiaoxin.get_or_create(sn=uuid.uuid4())
            user_xiaoxin = XiaoxinUser.get_or_create(user=user,xiaoxin=xx)
            user_xiaoxin.save()
            
        user.save()
        return "Ok"
    except Exception as e:
        debug(e)
        
    return "Fail"
    

def mobile_bind(form):
    try:
        _sn = getformValue(form,"sn")
        _userid =getformValue(form,"userid")
        usr = User.get(User.userid == _userid)
        xx = Xiaoxin.get(Xiaoxin.sn == _sn)
        user_xiaoxin = XiaoxinUser.get_or_create(user=usr,xiaoxin=xx)
        user_xiaoxin.save()
        return "Ok"
    except Exception as e:
        debug(e)
        
    return "Fail"

def mobile_rename(form):
    try:
        _sn = getformValue(form,"sn")
        _name =getformValue(form,"name")
 
        xx = Xiaoxin.get(Xiaoxin.sn == _sn)
        xx.name = _name;
        xx.save();

        return "Ok"
    except Exception as e:
        debug(e)
        
    return "Fail"
def mobile_unbind(form):
    try:
        _sn = getformValue(form,"sn")
        _userid =getformValue(form,"userid")
        usr = User.get(User.userid == _userid)
        xx = Xiaoxin.get(Xiaoxin.sn == _sn)
        user_xiaoxin = XiaoxinUser.get(XiaoxinUser.user==usr,XiaoxinUser.xiaoxin==xx)
        user_xiaoxin.delete_instance()
        return "Ok"
    except Exception as e:
        debug(e)
        
    return "Fail"

def mobile_query_bindlist(form):
    try:
        _userid =getformValue(form,"userid")
        usr = User.get(User.userid == _userid)
        ret="count=%d" % usr.xiaoxins.count();
        
        i=0
        for xx_usr in usr.xiaoxins:
            
            ret+="&sn%d=%s" % (i,xx_usr.xiaoxin.sn)
            i=i+1
        return ret
    except Exception as e:
        debug(e)
        
    return "Fail"    


def mobile_getxiaoxin(form):
    try:
        _sn = getformValue(form,"sn")
        xx = Xiaoxin.get(Xiaoxin.sn == _sn)
        return "name=%s&temp=%g&humi=%g&pm25=%g&switch=%d&speed=%d&form=%g&last_upload_time=%d" % (xx.name,xx.temp,xx.humi,xx.pm25,xx.switch,xx.speed,xx.form,int(xx.last_upload_time));
    except Exception as e:
        debug(e)
        

    return "Fail"
    
    
def mobile_setxiaoxin_switch(form):
    try:
        _sn = getformValue(form,"sn")
        _switch = getformValue(form,"switch")
        xx = Xiaoxin.get(Xiaoxin.sn == _sn)
        xx.switch = _switch
        xx.save()
        return "Ok"        
    except Exception as e:
        debug(e)
        

    return "Fail"

def mobile_setxiaoxin_speed(form):
    try:
        _sn = getformValue(form,"sn")
        _speed = getformValue(form,"speed")
        xx = Xiaoxin.get(Xiaoxin.sn == _sn)
        xx.speed = _speed
        xx.save()
        return "Ok"
    except Exception as e:
        debug(e)
        

    return "Fail"
@app.route('/mobile/<action>', methods=['GET', 'POST'])
def route_mobile(action):
    
    #return "Failed"
    if request.method == "GET":
        return print_mobile_help();
   
    info(action+":"+str(request.form))
    
    if action == "login":
        return mobile_login(request.form)
    elif action=="getxiaoxin":
        return mobile_getxiaoxin(request.form)
    elif action=="bind":
        return mobile_bind(request.form)
    elif action=="unbind":
        return mobile_unbind(request.form)
    elif action=="query_bindlist":
        return mobile_query_bindlist(request.form)
    elif action=="setxiaoxin_switch":
        return mobile_setxiaoxin_switch(request.form)
    elif action=="setxiaoxin_speed":
        return mobile_setxiaoxin_speed(request.form)
    elif action=="setxiaoxin_name":
        return mobile_rename(request.form)
    
    return "Fail"
