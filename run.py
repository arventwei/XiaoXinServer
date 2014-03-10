# -*- coding: utf-8 -*-
from flask import Flask
from app import app
from app.log import initLog


if __name__ == "__main__":
  
    initLog();
    app.run(host="0.0.0.0", port=9999, debug=True)
