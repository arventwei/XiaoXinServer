#!/usr/bin/python
from flask import request
from app import app


@app.route('/xiaoxin/<action>', methods=['GET', 'POST'])
def xiaoxin(action):
    #return "Failed"
    ret="==-=-=-=-=-=-=-="
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