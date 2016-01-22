'''
Created on Jan 21, 2016

@author: cmelton
'''

from celery import Celery
import os, sys

path = os.path.join(os.getcwd().split("DDServerApp")[0])
print path
if not path in sys.path:
    sys.path.insert(1, path)

app = Celery('CeleryApp', backend='rpc://', broker='amqp://guest@localhost//')

from DDServerApp.ORM.Mappers import orm, User, Workflow, WorkflowTemplate
SESSION= orm.loadSessionMaker()

@app.task
def add(x, y):
    return x + y

@app.task
def startWorkflow(wfid, logfilename, address, workflowname):
    wft = WorkflowTemplate.findByID(SESSION, wfid)
    return wft.startWorkflow(SESSION, logfilename, address, workflowname)

@app.task
def stopWorkflow(wfid):
    wft = WorkflowTemplate.findByID(SESSION, wfid)
    return wft.stopWorkflow(SESSION)