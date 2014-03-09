#!/usr/bin/python
from flask import request
from app import app


@app.route('/xiaoxin/<action>', methods=['GET', 'POST'])
def xiaoxin(action):
    #return "Failed"
    print request.json
    if request != None:
        print request.json
    print "=========================="
    #if action =="config":
    #    return xiaoxin_config(request.json)
    return "ok"
    #return "Hello, World !"+action

def xiaoxin_config(content):
    return content;
    #pass