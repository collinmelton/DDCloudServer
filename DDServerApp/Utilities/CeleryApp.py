'''
Created on Jan 21, 2016

@author: cmelton
'''

from celery import Celery

app = Celery('CeleryApp', backend='rpc://', broker='amqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y