#!/usr/bin/python
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
from models import xiaoxin,user,xiaoxin_user
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
    xiaoxin.create_table()
    user.create_table()
    xiaoxin_user.create_table()
    
@app.route('/')
def index():
    return 'Index Page'

from app import mobile
from app import xiaoxin
