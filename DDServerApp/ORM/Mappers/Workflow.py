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
#     
#     # takes a dictionary and replaces a variable in the specified dictionary
#     # entries with each replacement in a list of replacements
#     def _expandVar(self, dict, variable, replacements, keys=[]):
#         if keys==[]: keys = dict.keys()
#         dicts = []
#         for replacement in replacements:
#             newD = self.repDict(dict)
#             for key in keys:
#                 if type(newD[key]) is list:
#                     newD[key]=[x.replace(variable, replacement) for x in newD[key]]
#                 else:
#                     newD[key]=newD[key].replace(variable, replacement)
#             dicts.append(newD)
#         return dicts
#     
#     # takes a list of dictionaries and performs string replacement of variable
#     # and each replacement in a list of replacements for the specified set of
#     # keys
#     def _expandVars(self, dicts, variable, replacements, keys=[]):
#         result = []
#         for dict in dicts:
#             result+=self._expandVar(dict, variable, replacements, keys=keys)
#         return result
#     
#     # takes a dictionary and replaces tuples of (variable, replacements)
#     def _replaceVars(self, d, varsDict, keys=[]):
#         replacementTuples = [(key, map(lambda x: x.strip(), value.split(","))) for key, value in varsDict.items()]
#         dicts = [d]
#         for variable, replacements in replacementTuples:
#             dicts = self._expandVars(dicts, variable, replacements, keys=keys)
#         return dicts
    
    def _mergeDicts(self, dict1, dict2):
        result = self.repDict(dict1)
        for key, val in dict2.items(): result[key]=val
        return result
    
    # initialize disks and instances
    def initDisksAndInstances(self):
        # get disks
        self.disks = self.createDisksInNamedDict()
        # get instances
        self.instances = self.createInstancesInNamedDict(self.disks)
        # init instances with dependencies
        for instance in self.instances:
            instance.setDependencies(self.instances)
        
#     # creates disks
#     def createDisksInNamedDict(self):
#         diskTemplates = self.workflowtemplate.disktemplates
#         workflowVars = self.workflowtemplate.workflow_vars
#         diskParamDicts = []
#         for dt in diskTemplates:
#             diskVars = dt.disk_vars
#             diskParamDict = {"name": dt.name,
#                              "size": dt.disk_size,
#                              "location": dt.location,
#                              "image": dt.image.name,
#                              "disk_type": dt.disk_type} 
#             varsDict = self._mergeDicts(diskVars, workflowVars)
#             diskParamDicts+=self._replaceVars(diskParamDict, varsDict, keys=["name"])       
#         # make disk instances
#         result={}
#         for diskParamDict in diskParamDicts:
#             result[diskParamDict['name']] = Disk(diskParamDict["name"], diskParamDict["size"], 
#                                                diskParamDict["location"], snapshot=None, 
#                                                image=diskParamDict["image"], instanceNames=[], 
#                                                disk_type = diskParamDict["disk_type"], 
#                                                init_source="", shutdown_dest="", myDriver=None, log=None) 
#         return result

    # creates disks
    def createDisksInNamedDict(self):
        diskTemplates = self.workflowtemplate.disktemplates
        print diskTemplates
        workflowVars = self.workflowtemplate.workflow_vars
        disks = {}
        for dt in diskTemplates:
            varsDict = self._mergeDicts(dt.disk_vars, workflowVars)
            newdisks = dt.generateDisks(varsDict)
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
    

    
#     # creates instance objects
#     def createInstancesInNamedDict(self, disks):
#         instanceTemplates = self.workflowtemplate.instancetemplates
#         workflowVars = self.workflowtemplate.workflow_vars
# 
#         result = {}
#         for it in instanceTemplates:
#             instanceVars = it.variables
#             variableDicts = self._parseVariableDicts(self._mergeDicts(instanceVars, workflowVars)) 
#             for variableDict in variableDicts:
#                 instanceParamDict = it.getParamDict(variableDict)
#                 commandDict = instanceParamDict["commands"]
#                 # get standard node params
#                 node_params={}
#                 for param in ["size", "image", "location", "ex_network"]:
#                     node_params[param]=instanceParamDict[param]
#                 # parse ex_tags
#                 node_params["ex_tags"]=instanceParamDict["ex_tags"].split("|")
#                 # parse ex_metadata and add to node params
#                 node_params["ex_metadata"]={'items': []}
#                 for pair in instanceParamDict["ex_metadata"].split("|"):
#                     if pair!="":
#                         key, value= pair.split(":")
#                         node_params["ex_metadata"]["items"].append({"key":key, "value":value})
#                     
#                 # get read disks and boot disk
#                 read_disks=[]
#                 for rd in instanceParamDict["read_disks"]:
#                     if rd not in disks: raise Exception("read disk not found:"+rd) 
#                     read_disks.append(disks[rd])
#                     disks[rd].addInstance(instanceParamDict['name'])
#                 read_write_disks=[]
#                 for rd in instanceParamDict["read_write_disks"]:
#                     if rd not in disks: raise Exception("read/write disk not found:"+rd) 
#                     read_write_disks.append(disks[rd])
#                     disks[rd].addInstance(instanceParamDict['name'])
#                 if instanceParamDict["boot_disk"] not in disks: raise Exception("boot disk not found:"+instanceParamDict["boot_disk"])
#                 boot_disk=disks[instanceParamDict["boot_disk"]]
#                 boot_disk.addInstance(instanceParamDict['name'])
#                 
#                 # add new instance
#                 result[instanceParamDict['name']]=Instance(instanceParamDict["name"], node_params, 
#                                                            instanceParamDict["dependencies"], 
#                                                            read_disks, read_write_disks, boot_disk,
#                                                            commandDict, rootdir="/home/cmelton/", 
#                                                            preemptible=instanceParamDict["preemptible"],  
#                                                            numLocalSSD=instanceParamDict["numLocalSSD"], 
#                                                            localSSDInitSources="", localSSDDests="")
#         return result
    
    @staticmethod
    def findByName(session, name, user):
        wfs=session.query(Workflow).filter(Workflow.workflowname==name).filter(Workflow.user_id==user.id).all()
        if len(wfs)==0: return None
        else: return wfs[0]
    