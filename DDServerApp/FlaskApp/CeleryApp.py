'''
Created on Jan 21, 2016

@author: cmelton
'''

from celery import Celery, Task
import os, sys, time

path = os.path.join(os.getcwd().split("DDServerApp")[0])
print path
if not path in sys.path:
    sys.path.insert(1, path)

app = Celery('CeleryApp', backend='rpc://', broker='amqp://guest@localhost//')

from DDServerApp.ORM.Mappers import orm, WorkflowTemplate, Instance
SESSION= orm.loadSessionMaker()

class SqlAlchemyTask(Task):
    """An abstract Celery Task that ensures that the connection the the
    database is closed on task completion"""
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        SESSION.remove()





@app.task(base=SqlAlchemyTask)
def add(x, y):
    return x + y

@app.task(base=SqlAlchemyTask)
def startWorkflow(wfid, logfilename, address, workflowname):
    wft = WorkflowTemplate.findByID(SESSION, wfid)
    return wft.startWorkflow(SESSION, logfilename, address, workflowname)

@app.task(base=SqlAlchemyTask)
def stopWorkflow(wfid):
    wft = WorkflowTemplate.findByID(SESSION, wfid)
    return wft.stopWorkflow(SESSION)

@app.task(base=SqlAlchemyTask)
def finishInstance(iid):
    instance = Instance.findByID(SESSION, iid)
    instance.finish(SESSION)

@app.task(base=SqlAlchemyTask)
def restartInstance(iid):
    time.sleep(60)
    instance = Instance.findByID(SESSION, iid)
    return instance.restart(SESSION)

