#!/usr/bin/python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

from app import mobile
from app import xiaoxin
