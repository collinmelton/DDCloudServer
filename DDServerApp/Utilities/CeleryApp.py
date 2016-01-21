'''
Created on Jan 21, 2016

@author: cmelton
'''

from celery import Celery

app = Celery('CeleryApp', backend='rpc://', broker='amqp://guest@localhost//')

from DDServerApp.ORM.Mappers import orm, User, Workflow
SESSION= orm.loadSessionMaker()

@app.task
def add(x, y):
    return x + y

@app.task
def startWorkflow(wfid, logfilename, address, workflowname):
    wf = Workflow.findByID(SESSION, wfid)
    return wf.startWorkflow(SESSION, logfilename, address, workflowname)

@app.task
def stopWorkflow(wfid):
    wf = Workflow.findByID(SESSION, wfid)
    return wf.stopWorkflow(SESSION)