#!/usr/bin/python
# -*- coding: utf-8 -*-
from app import app

@app.route('/mobile')
def mobile():
    return "Hello, World mobile!"
