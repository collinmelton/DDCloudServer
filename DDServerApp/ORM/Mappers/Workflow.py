'''
Created on Nov 20, 2015

@author: cmelton
'''

# imports
from DDServerApp.ORM import orm,Column,relationship,String,Integer, PickleType, Float,ForeignKey,backref,TextReader, joinedload_all
from DDServerApp.ORM import BASE_DIR, Boolean
import sys, time, copy, thread, datetime, inspect
from DDServerApp.ORM.Mappers import User, WorkflowTemplate, Disk, Instance
from DDServerApp.Utilities.GCEManager import GCEManager 

VERBOSE = True

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

class LogFile(orm.Base):
    '''
    This class logs data.
    '''
    id = Column(Integer,primary_key=True)
    fileName = Column(String, index=True)
    
    def __init__(self, fileName):
        self.fileName=fileName
        self.lock=thread.allocate_lock()
        try:
            f = open(self.fileName, 'w')
            f.write("logfile start")
            f.close()
        except:
            print "something is wrong with log file"

    def _reallocateLockIfNeeded(self):
        if "lock" not in self.__dict__: self.lock=thread.allocate_lock()
    
    def __str__(self):
        return self.fileName

    # write with new line and date-time
    def write(self, textToWrite):
        self._reallocateLockIfNeeded()
        self.lock.acquire()
        f = open(self.fileName, 'a')
        # write time then add text to write
        f.write("\n"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+"\t")
        f.write(str(textToWrite))
        if VERBOSE: print "log: ", textToWrite
        if f: f.close()
        self.lock.release()
    
    # write without date or newlines etc
    def writeRaw(self, textToWrite):
        self._reallocateLockIfNeeded()
        self.lock.acquire()
        try:
            f = open(self.fileName, 'a')
            # write time then add text to write
            f.write(textToWrite)
            if VERBOSE: print textToWrite
            if f: f.close()
        except:
            if VERBOSE: print "something is wrong with raw log file writing"
        self.lock.release()
    
class GCEManagerBinding(orm.Base):
    '''
    This class links an ORM version to the non ORM manager.
    '''
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    key = Column(String)
    auth_account = Column(String)
    datacenter = Column(String)
    project = Column(String)
    auth_type = Column(String)
    extraArgs = Column(PickleType)
    
    def __init__(self, user_id, key, auth_account=None, datacenter=None, project=None,
                 auth_type=None, **kwargs):
        self.user_id = user_id
        self.auth_account = auth_account
        self.key = key
        self.datacenter = datacenter
        self.project = project
        self.auth_type = auth_type
        self.extraArgs = kwargs
        self.manager = self._ensureManagerExists()
    
    def _ensureManagerExists(self):
        import Crypto
        Crypto.Random.atfork()
        if "manager" not in self.__dict__ or self.manager==None: 
            if VERBOSE: print "making manager"
            self.manager = GCEManager(self.user_id, self.key, datacenter=self.datacenter, 
                                      project=self.project, auth_type=self.auth_type)
            if VERBOSE: print self.manager
#         , **self.extraArgs)
    
    def runCommand(self, command, *args, **kwargs):
        self._ensureManagerExists()
        methods = [m for m in inspect.getmembers(self.manager) if m[0]==command]
        if methods == []: 
            if VERBOSE: print inspect.getmembers(self.manager)
            if VERBOSE: print "error in running command in GCE Manager Binding!"
        else: return methods[0][1](*args, **kwargs)
    
    def list_nodes(self, *args, **kwargs):
        return self.runCommand("list_nodes", *args, **kwargs)
        
    def list_images(self, *args, **kwargs):
        return self.runCommand("list_images", *args, **kwargs)
        
    def list_volumes(self, *args, **kwargs):
        return self.runCommand("list_volumes", *args, **kwargs)
    
    def create_node(self, *args, **kwargs):
        if VERBOSE: print "creating node, project:", self.project
        return self.runCommand("create_node", *args, **kwargs)
        
    def ex_get_node(self, *args, **kwargs):
        return self.runCommand("ex_get_node", *args, **kwargs)
        
    def destroy_node(self, *args, **kwargs):
        return self.runCommand("destroy_node", *args, **kwargs)
        
    def create_volume(self, *args, **kwargs):
        return self.runCommand("create_volume", *args, **kwargs)
        
    def ex_get_volume(self, *args, **kwargs):
        return self.runCommand("ex_get_volume", *args, **kwargs)
        
    def destroy_volume(self, *args, **kwargs):
        return self.runCommand("destroy_volume", *args, **kwargs)
        
    def detach_volume(self, *args, **kwargs):
        return self.runCommand("detach_volume", *args, **kwargs)
    
class Workflow(orm.Base):
    '''
    This class represents an instance to be run on the Google Compute Engine.
    '''
    id = Column(Integer,primary_key=True)
    workflowname = Column(String, index=True)
    workflowtemplate_id = Column(Integer, ForeignKey("workflowtemplate.id"))
    workflowtemplate = relationship(WorkflowTemplate, backref = "workflows")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User, backref = "workflows")
    active = Column(Boolean)
    instances = relationship(Instance, secondary='instanceworkflowlink', backref="workflows")
    disks = relationship(Disk, secondary='diskworkflowlink', backref="workflows")
    logfile_id = Column(Integer, ForeignKey("logfile.id"))
    logfile = relationship(LogFile, backref = "workflows")
    gce_manager_id = Column(Integer, ForeignKey("gcemanagerbinding.id"))
    gce_manager = relationship(GCEManagerBinding, backref = "workflows")
    address = Column(String)
    name = Column(String)

    def __init__(self, name, workflowtemplate, user, logfilename, address, gceManagerExtraArgs = {}):
        '''
        Constructor
        '''
        self.name=name
        self.workflowtemplate = workflowtemplate
        self.user = user
        self.active = False
        if VERBOSE: print "adding logfile"
        self.logfile = LogFile(logfilename)
        if VERBOSE: print "adding manager"
        self.gce_manager = GCEManagerBinding(self.workflowtemplate.credentials.serviceAccount, 
                                             self.workflowtemplate.credentials.pemFileLocation, 
                                             project = self.workflowtemplate.credentials.project,
                                             auth_type=None, **gceManagerExtraArgs)
        if VERBOSE: print "added manager"
        self.address = address
    
    def dictForJSON(self):
        return {"id": str(self.id),
                "name": self.name}
    
    # a unique name for GCE
    def gce_name(self):
        return "-".join(map(str, [self.workflowtemplate.id, self.id, self.workflowname]))
    
    # starts the workflow
    def start(self, session):
        self.active = True
        if VERBOSE: print "set to active"
#         print "images", self.gce_manager.list_images()
#         print self.gce_manager.create_volume(10, "test", location="us-central1-a", snapshot=None, image="cloudtest110915", ex_disk_type="pd-standard")
        
        if VERBOSE: print "initializing disks and instances"
        self.initDisksAndInstances()
         
        if VERBOSE: print "starting instances if ready"
        for instance in self.instances:
            instance.startIfReady(session)
            
    def stop(self):
        self.active = False
        return
        for instance in self.instances: 
            if instance.created and not instance.destroyed:
                instance.destroy(destroydisks=False, force = False)
                if not instance.destroyed: instance.destroy(destroydisks=False, force = True)
        for disk in self.disks:
            if disk.created and not disk.destroyed: disk.destroy()
    
#     # adds myDriver, instance, and log to instance
#     def reinit(self, myDriver, log):
#         self.myDriver = myDriver
#         self.log = log

    # string output
    def __str__(self):
        return "workflow object: "+self.gce_name()
    
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
            newdisks = dt.generateDisks(workflowVars, gce_manager=self.gce_manager, log = self.logfile)
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
            newinstances = it.generateInstances(varDict, disks, gce_manager=self.gce_manager, log = self.logfile)
            instances = self._mergeDicts(instances, newinstances)
        return instances
    
    @staticmethod
    def findByName(session, name, user):
        wfs=session.query(Workflow).filter(Workflow.workflowname==name).filter(Workflow.user_id==user.id).all()
        if len(wfs)==0: return None
        else: return wfs[0]
    