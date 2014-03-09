#!/usr/bin/python
from app import app


@app.route('/xiaoxin')
def xiaoxin():
    return "Hello, World!"
