#!/usr/bin/python
from app import app

@app.route('/mobile')
def mobile():
    return "Hello, World mobile!"
