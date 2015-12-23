'''
Created on Nov 20, 2015

@author: cmelton
'''

# imports
from DDServerApp.ORM import orm,Column,relationship,String,Integer, PickleType, Float,ForeignKey,backref,TextReader, joinedload_all
from DDServerApp.ORM import BASE_DIR, Boolean
import sys, time, copy
from DDServerApp.ORM.Mappers import User, WorkflowTemplate, Disk, Instance


class DiskWorkflowLink(orm.Base):
    '''
    This relation maps many disks to many instances.
    '''
    disk_id = Column(Integer, ForeignKey('disk.id'), primary_key=True)
    workflow_id = Column(Integer, ForeignKey('workflow.id'), primary_key=True)
    
class InstanceWorkflowLink(orm.Base):
    '''
    This relation maps many disks to many instances.
    '''
    workflow_id = Column(Integer, ForeignKey('workflow.id'), primary_key=True)
    instance_id = Column(Integer, ForeignKey('instance.id'), primary_key=True)
    
    
class Workflow(orm.Base):
    '''
    This class represents an instance to be run on the Google Compute Engine.
    '''
    id = Column(Integer,primary_key=True)
    workflowname = Column(String, index=True)
    workflowtemplate_id = Column(Integer, ForeignKey("workflowtemplate.id"))
    workflowtemplate = relationship(WorkflowTemplate, backref = "workflowtemplates")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User, backref = "workflows")
    active = Column(Boolean)
    instances = relationship(Instance, secondary='instanceworkflowlink')
    disks = relationship(Disk, secondary='diskworkflowlink')

    def __init__(self, name, workflowtemplate, user):
        '''
        Constructor
        '''
        self.name=name
        self.workflowtemplate = workflowtemplate
        self.user = user
        self.active = False
    
    # a unique name for GCE
    def name(self):
        return "-".join(map(str, [self.workflowtemplate.id, self.id, self.workflowname]))
    
    # starts the workflow
    def start(self):
        self.active = True
    
    # adds myDriver, instance, and log to instance
    def reinit(self, myDriver, log):
        self.myDriver = myDriver
        self.log = log

    # string output
    def __str__(self):
        return "workflow object: "+self.name()
    
    # representation output
    def __repr__(self):
        return str(self)
    
    # replicates a dictionary
    def repDict(self, x):
        return copy.copy(x)
    
    def _mergeDicts(self, dict1, dict2):
        result = self.repDict(dict1)
        for key, val in dict2.items(): result[key]=val
        return result
    
    # initialize disks and instances
    def initDisksAndInstances(self):
        # get disks
        disks = self.createDisksInNamedDict()
        self.disks = disks.values()
        # get instances
        instances = self.createInstancesInNamedDict(disks)
        self.instances = instances.values()
        # init instances with dependencies
        for instance in self.instances:
            instance.setDependencies(instances)

    # creates disks
    def createDisksInNamedDict(self):
        diskTemplates = self.workflowtemplate.disktemplates
        workflowVars = self.workflowtemplate.workflow_vars
        disks = {}
        for dt in diskTemplates:
#             varsDict = self._mergeDicts(dt.disk_vars, workflowVars)
            newdisks = dt.generateDisks(workflowVars)
            disks = self._mergeDicts(disks, newdisks)
        return disks
    
    # makes a copy of a list of dictionaries
    def _repDicts(self, alist):
        return [self.repDict(x) for x in alist]
    
    # creates a separate dictionary for every combination of variables in varDict
    def _parseVariableDicts(self, varDict):
        replacementTuples = [(key, map(lambda x: x.strip(), value.split(","))) for key, value in varDict.items()]
        result = [{}]
        for variable, replacements in replacementTuples:
            newresult = []
            for replacement in replacements:
                dictsToAdd = self._repDicts(result)
                for dictToAdd in dictsToAdd:
                    dictToAdd[variable]=replacement
                newresult += dictsToAdd
            result = newresult
        return result

    # creates instance objects
    def createInstancesInNamedDict(self, disks):
        instanceTemplates = self.workflowtemplate.instancetemplates
        workflowVars = self.workflowtemplate.workflow_vars
        instances = {}
        for it in instanceTemplates:
            varDict = self._mergeDicts(it.variables, workflowVars)
            newinstances = it.generateInstances(varDict, disks)
            instances = self._mergeDicts(instances, newinstances)
        return instances
    
    @staticmethod
    def findByName(session, name, user):
        wfs=session.query(Workflow).filter(Workflow.workflowname==name).filter(Workflow.user_id==user.id).all()
        if len(wfs)==0: return None
        else: return wfs[0]
    