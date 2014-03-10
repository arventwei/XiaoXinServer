#!/usr/bin/python
# -*- coding: utf-8 -*-  
from flask import request
from app import app
from log import info,debug,log
from models import xiaoxin,user
#test data
#curl --data "birthyear=1905&press=%20OK%20" http://127.0.0.1:9999/xiaoxin/config
#
def print_help():
    ret =  """
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
    3.接口类型如下：<br>
       3.1 小新配置接口 ，当小新的设置按钮按下时，小新等待手机的WIFI配置信息，<br>
       3.2 当小新配置完毕后，连接网络，第一件事，就是保存sn和userid，并把这两个值发给服务器。<br>
       3.3 发送格式如下 sn=123456123&userid=sina_123456 ,注意 sn和userid都是小写<br>
       3.4 测试例子：<br>
       curl --data "sn=123456123&userid=sina_123456" http://127.0.0.1:9999/xiaoxin/config<br>
    """;
    
    return ret;
    
def getformValue(form,name):
    if name not in form:
        debug(name+" is null");
        return False,""
    return True,form[name]
@app.route('/xiaoxin/<action>', methods=['GET', 'POST'])
def xiaoxin(action):
    
    #return "Failed"
    if request.method == "GET":
        return print_help();
   
    info(request.form)
    
    ret_sn,sn = getformValue(request.form,"sn")
    ret_userid,userid =getformValue(request.form,"userid")
    
    if not ret_sn  or  not ret_userid:
        return "Fail"
    
    
    
    #sn = request.form["sn"]
    #userid =request.form["userid"]
   
    #info(request.form)
    
   # print request.json
    #if request != None:
     #   ret+= str(request.data).lower()
    #ret+= "=========================="
    #if action =="config":
    #    return xiaoxin_config(request.json)
    #return ret
    #return "Hello, World !"+action

def xiaoxin_config(content):
    return content;
    #pass