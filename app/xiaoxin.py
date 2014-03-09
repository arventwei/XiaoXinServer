#!/usr/bin/python
from flask import request
from app import app
from log import info
#test data
#curl --data "birthyear=1905&press=%20OK%20" http://127.0.0.1:9999/xiaoxin/config
#
@app.route('/xiaoxin/<action>', methods=['GET', 'POST'])
def xiaoxin(action):
    #return "Failed"
    
    ret="Ok"
    if "sn" not in request.form:
        return "Fail sn is null"
    sn = request.form["sn"]
    userid =request.form["userid"]
   
        
    if userid == None:
        return "Fail userid is null";
    info(request.form)
   # print request.json
    if request != None:
        ret+= str(request.data).lower()
    ret+= "=========================="
    #if action =="config":
    #    return xiaoxin_config(request.json)
    return ret
    #return "Hello, World !"+action

def xiaoxin_config(content):
    return content;
    #pass