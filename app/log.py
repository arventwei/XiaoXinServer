# -*- coding: utf-8 -*-
import logging


def initLog():
    print "init Log"
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)


    fh = logging.FileHandler('test.log')
    fh.setLevel(logging.DEBUG)
    
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    
    logger.addHandler(fh)
    logger.addHandler(ch)

def info(content):
    logger = logging.getLogger('mylogger')
    logger.info(content)
def debug(content):
    logger = logging.getLogger('mylogger')
    logger.debug(content)
def error(content):
    logger = logging.getLogger('mylogger')
    logger.error(content)
def log(content):
    logger = logging.getLogger('mylogger')
    logger.log(content)