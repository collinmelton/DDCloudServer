'''
Created on Dec 11, 2015

@author: cmelton
'''

from DDServerApp.ORM import orm,Column,relationship,String,Integer, PickleType, Float,ForeignKey,backref,TextReader, joinedload_all
from DDServerApp.ORM import BASE_DIR, Boolean
from User import User
import os, copy

class Credentials(orm.Base):
    '''
    classdocs
    '''
    id = Column(Integer,primary_key=True)
    name = Column(String)
    serviceAccount = Column(String)
    pemFileLocation = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User, backref=backref("credentials"))
    project = Column(String)

    def __init__(self, name, serviceAccount, pemFileLocation, project, user):
        '''
        Constructor
        '''
        self.name = name
        self.user = user
        self.serviceAccount = serviceAccount
        self.pemFileLocation = pemFileLocation 
        self.project = project
        
    def dictForJSON(self):
        return {"id": str(self.id),
                "name": self.name, 
                "serviceaccount": self.serviceAccount,
                "project": self.project
                }

    def updateValues(self, name, serviceAccount, pemFileLocation, project):
        self.name = name
        self.serviceAccount = serviceAccount
        if os.path.exists(self.pemFileLocation):
            os.remove(self.pemFileLocation)
        self.pemFileLocation = pemFileLocation
        self.project = project

    @staticmethod
    def findByID(session, cid, user):
        cids=session.query(Credentials).join(User).filter(Credentials.id==int(cid)).filter(User.id==user.id).all()
        if len(cids)==0: return None
        else: return cids[0]

    @staticmethod
    def findByName(session, name, user):
        creds=session.query(Credentials).filter(Credentials.name==name).filter(Credentials.user_id==user.id).all()
        if len(creds)==0: return None
        else: return creds[0]
        
    @staticmethod
    def delete(session, cid, user):
        cred = Credentials.findByID(session, cid, user)
        if cred != None:
            session.delete(cred)
            session.commit()

class WorkflowTemplate(orm.Base):
    '''
    Class to hold user defined workflow. Its a template because
    it can be used to create a workflow at runtime.
    '''
    id = Column(Integer,primary_key=True)
    name = Column(String)
    workflow_vars = Column(PickleType)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User, backref = "workflowtemplates")
    credentials_id = Column(Integer, ForeignKey("credentials.id"))
    credentials = relationship(Credentials, backref = "workflowtemplates")

    def __init__(self, name, user, workflowVars={}, credentials = None):
        '''
        Constructor
        '''
        self.name = name
        self.user = user
        self.workflow_vars = workflowVars
        self.credentials = credentials 
    
    def isActive(self):
        return any([wf.active for wf in self.workflows])
    
    def startWorkflow(self, session, logfilename, address, workflowname):
        from Workflow import Workflow
        print "imported"
        if not self.isActive():
            print workflowname
            wf = Workflow(workflowname, self, self.user, logfilename, address)
            session.add(wf)
            session.commit()
            "print not active found workflow"
            wf.start(session)
            print "starting workflow"
            session.add(wf)
            session.commit()
    
    def stopWorkflow(self, session):
        for wf in self.workflows:
            wf.stop()
        session.add_all(self.workflows)
        session.commit()
    
    def _instancesToDictForJSON(self):
        return {str(inst.id): inst.dictForJSON() for inst in self.instancetemplates}
    
    def _disksToDictForJSON(self):
        return {str(disk.id): disk.dictForJSON() for disk in self.disktemplates}
    
    def dictForJSON(self):
        return {"id": str(self.id),
                "name": self.name,
                "variables": self.workflow_vars,
                "instances": self._instancesToDictForJSON(),
                "disks": self._disksToDictForJSON(),
                "credentials": self.credentials_id}
    
    def updateVarDict(self, vardict, user):
        if self.user == user:
            self.workflow_vars = {}
            for key in vardict:
                self._addVars(key, vardict[key])
    
    def _addVars(self, key, value):
        self.workflow_vars[key]=value
    
    @staticmethod
    def findByID(session, wfid, user=None):
        if user == None:
            wfs=session.query(WorkflowTemplate).filter(WorkflowTemplate.id==int(wfid)).all()
        else:
            wfs=session.query(WorkflowTemplate).filter(WorkflowTemplate.id==int(wfid)).filter(WorkflowTemplate.user_id==user.id).all()
        if len(wfs)==0: return None
        else: return wfs[0]
        
    @staticmethod
    def findByName(session, name, user):
        wfs=session.query(WorkflowTemplate).filter(WorkflowTemplate.name==name).filter(WorkflowTemplate.user_id==user.id).all()
        if len(wfs)==0: return None
        else: return wfs[0]
        
    @staticmethod
    def delete(session, wfid, user):
        workflow = WorkflowTemplate.findByID(session, wfid, user)
        if workflow != None:
            session.delete(workflow)
            session.commit()
#         session.query(WorkflowTemplate).filter(WorkflowTemplate.id==wfid).filter(WorkflowTemplate.user_id==user.id).delete()


class Image(orm.Base):
    '''
    classdocs
    '''
    id = Column(Integer,primary_key=True)
    name = Column(String)
    authAccount = Column(String)
    rootdir = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User, backref = "images")
    
    def __init__(self, name, authAccount, rootdir, user):
        '''
        Constructor
        '''
        self.name = name
        self.authAccount = authAccount
        self.user = user
        self.rootdir = rootdir

    def dictForJSON(self):
        return {"id": str(self.id),
                "name": self.name,
                "authaccount": self.authAccount,
                "installDirectory": self.rootdir}

    def updateValues(self, name, authAccount, rootdir, user):
        if self.user == user:
            self.name = name
            self.authAccount = authAccount
            self.rootdir = rootdir

    @staticmethod
    def findByID(session, iid, user):
        images=session.query(Image).join(User).filter(Image.id==int(iid)).filter(User.id==user.id).all()
        if len(images)==0: return None
        else: return images[0]

    @staticmethod
    def findByName(session, name, user):
        images=session.query(Image).join(User).filter(Image.name==name).filter(User.id==user.id).all()
        if len(images)==0: return None
        else: return images[0]
        
    @staticmethod
    def delete(session, iid, user):
        image = Image.findByID(session, iid, user)
        if image != None:
            session.delete(image)
            session.commit()
#         session.query(Image).filter(Image.id==iid).filter(Image.user_id==user.id).delete()

class DiskTemplate(orm.Base):
    '''
    classdocs
    '''
    id = Column(Integer,primary_key=True)
    name = Column(String)
    workflow_id = Column(Integer, ForeignKey("workflowtemplate.id"))
    workflow = relationship(WorkflowTemplate, backref = "disktemplates")
    image_id = Column(Integer, ForeignKey("image.id"))
    image = relationship(Image)
    disk_size = Column(Integer)
    disk_type = Column(String)
    location = Column(String)
    disk_vars = Column(PickleType)

    def __init__(self, name, workflow, image, disk_size, disk_type, location):
        '''
        Constructor
        '''
        self.name = name
        self.workflow = workflow
        self.image = image
        self.disk_size = disk_size
        self.disk_type = disk_type
        self.location = location
        self.disk_vars = {}
        
    def dictForJSON(self):
        return {"id": str(self.id),
              "name": self.name,
              "location": self.location,
              "disktype": self.disk_type,
              "size": str(self.disk_size),
              "image": str(self.image.id) if self.image!=None else None,
              "variables": self.disk_vars}
    
    def updateVarDict(self, vardict, user):
        if self.workflow.user == user:
            self.disk_vars = {}
            for key in vardict:
                self._addVars(key, vardict[key])
    
    def _addVars(self, key, value):
        self.disk_vars[key]=value
    
    def updateValues(self, name, workflow, image, diskSize, diskType, location, user):
        if self.workflow.user == user:
            self.name = name
            self.workflow = workflow
            self.image = image
            self.disk_size = diskSize
            self.disk_type = diskType
            self.location = location

    def _substituteVariables(self, x, varDict):
        for k, v in varDict.items():
            x = x.replace(k, v)
        return x

    # makes a copy of a list of dictionaries
    def _repDicts(self, alist):
        return [copy.copy(x) for x in alist]
    
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

    def _mergeDicts(self, dict1, dict2):
        result = copy.copy(dict1)
        for key, val in dict2.items(): result[key]=val
        return result

    def generateDisks(self, varDict, gce_manager=None, log = None):
        variableDicts = self._parseVariableDicts(self._mergeDicts(varDict, self.disk_vars))
        result = {}
        from DDServerApp.ORM.Mappers import Disk
        for variableDict in variableDicts:
            name = self._substituteVariables(self.name, variableDict)
            result[name] = Disk(name, self.disk_size, self.location, snapshot=None, image=self.image, 
                                disk_type = 'pd-standard', init_source="", shutdown_dest="",
                                gce_manager=gce_manager, log = log)
        return result  
        
    @staticmethod
    def findByID(session, did, user):
        ds=session.query(DiskTemplate).join(WorkflowTemplate).filter(DiskTemplate.id==int(did)).filter(WorkflowTemplate.user_id==user.id).all()
        if len(ds)==0: return None
        else: return ds[0]
        
    @staticmethod
    def findByName(session, name, user):
        ds=session.query(DiskTemplate).join(WorkflowTemplate).filter(DiskTemplate.name==name).filter(WorkflowTemplate.user_id==user.id).all()
        if len(ds)==0: return None
        else: return ds[0]
        
    @staticmethod
    def delete(session, did, user):
        disk = DiskTemplate.findByID(session, did, user)
        if disk != None:
            session.delete(disk)
            session.commit()
#         session.query(DiskTemplate).join(WorkflowTemplate).filter(DiskTemplate.id==did).filter(WorkflowTemplate.user_id==user.id).delete()

class ReadDiskLink(orm.Base):
    disktemplate_id = Column(Integer, ForeignKey('disktemplate.id'), primary_key=True)
    instancetemplate_id = Column(Integer, ForeignKey('instancetemplate.id'), primary_key=True)

class ReadWriteDiskLink(orm.Base):
    disktemplate_id = Column(Integer, ForeignKey('disktemplate.id'), primary_key=True)
    instancetemplate_id = Column(Integer, ForeignKey('instancetemplate.id'), primary_key=True)



class InstanceTemplateDependencyRelation(orm.Base):
    child_id = Column(Integer, ForeignKey('instancetemplate.id'), primary_key=True)
    parent_id = Column(Integer, ForeignKey('instancetemplate.id'), primary_key=True)

    
class InstanceTemplate(orm.Base):
    '''
    classdocs
    '''
    id = Column(Integer,primary_key=True)
    name = Column(String)
    workflow_id = Column(Integer, ForeignKey("workflowtemplate.id"))
    workflow = relationship(WorkflowTemplate, backref = "instancetemplates")
    machine_type = Column(String)
    location = Column(String)
    boot_disk_id = Column(Integer, ForeignKey("disktemplate.id"))
    boot_disk = relationship(DiskTemplate)
    read_disks = relationship(DiskTemplate, secondary='readdisklink')
    read_write_disks = relationship(DiskTemplate, secondary='readwritedisklink')
    # commands are backreferenced
    dependencies = relationship("InstanceTemplate", secondary='instancetemplatedependencyrelation',
                            primaryjoin=id==InstanceTemplateDependencyRelation.parent_id,
                            secondaryjoin=id==InstanceTemplateDependencyRelation.child_id,
                            backref="next_instances")
    variables = Column(PickleType)
    ex_tags = Column(String)
    ex_metadata = Column(String)
    ex_network = Column(String)
    numLocalSSD = Column(Integer)
    preemptible = Column(Boolean)

    def __init__(self, name, machine_type, location, boot_disk, read_disks, 
                 read_write_disks, dependencies, workflow, ex_tags, ex_metadata,
                 ex_network, numLocalSSD, preemptible):
        '''
        Constructor
        '''
        self.name = name
        self.machine_type = machine_type
        self.location = location
        self.boot_disk = boot_disk
        self.read_disks = read_disks
        self.read_write_disks = read_write_disks
        self.dependencies = dependencies
        self.variables = {}
        self.workflow = workflow
        self.ex_tags = ex_tags
        self.ex_metadata = ex_metadata
        self.ex_network = ex_network
        self.numLocalSSD = int(numLocalSSD)
        self.preemptible = preemptible
    
    def dictForJSON(self):
#         if "commandtemplates" in self.__dict__: commands = self.commandtemplates
#         else: commands = []
        return {"id": str(self.id),
              "name": self.name,
              "Commands": {str(c.id): c.dictForJSON() for c in self.commandtemplates},
              "BootDisk": str(self.boot_disk.id),
              "ReadDisks": [str(rd.id) for rd in self.read_disks],
              "WriteDisks": [str(wd.id) for wd in self.read_write_disks],
              "variables": self.variables,
              "machinetype": self.machine_type,
              "location": self.location,
              "dependencies": [str(d.id) for d in self.dependencies],
              "ex_tags": self.ex_tags,
              "ex_metadata": self.ex_metadata,
              "ex_network": self.ex_network,
              "numLocalSSD": self.numLocalSSD,
              "preemptible": self.preemptible}

    def _replaceVars(self, x, varDict):
        if type(x)==list:
            return [self._replaceVars(xi, varDict) for xi in x]
        for var, rep in varDict.items():
            x = x.replace(var, rep)
        return x

    def updateValues(self, name, machineType, location, bootDisk, read_disks, 
                     read_write_disks, dependencies, ex_tags, ex_metadata,
                     ex_network, numLocalSSD, preemptible):
        self.name = name
        self.machine_type = machineType
        self.location = location
        self.boot_disk = bootDisk
        self.read_disks = read_disks
        self.read_write_disks = read_write_disks
        self.dependencies = dependencies
        self.ex_tags = ex_tags
        self.ex_metadata = ex_metadata
        self.ex_network = ex_network
        self.numLocalSSD = int(numLocalSSD)
        self.preemptible = preemptible

    def updateVarDict(self, vardict, user):
        if self.workflow.user == user:
            self.variables = {}
            for key in vardict:
                self._addVars(key, vardict[key])
    
    def _addVars(self, key, value):
        self.variables[key]=value

    def _substituteVariables(self, x, varDict):
        for k, v in varDict.items():
            x = x.replace(k, v)
        return x

    # makes a copy of a list of dictionaries
    def _repDicts(self, alist):
        return [copy.copy(x) for x in alist]
    
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

    def _mergeDicts(self, dict1, dict2):
        result = copy.copy(dict1)
        for key, val in dict2.items(): result[key]=val
        return result

    def generateInstances(self, varDict, disks, gce_manager=None, log = None):
        variableDicts = self._parseVariableDicts(self._mergeDicts(varDict, self.variables))
        result = {}
        from DDServerApp.ORM.Mappers import Instance
        for variableDict in variableDicts:
            name = self._substituteVariables(self.name, variableDict)
            dependency_names = [self._substituteVariables(d.name, variableDict) for d in self.dependencies]
            read_disks = [disks[self._substituteVariables(d.name, variableDict)] for d in self.read_disks]
            read_write_disks = [disks[self._substituteVariables(d.name, variableDict)] for d in self.read_write_disks]
            boot_disk = disks[self._substituteVariables(self.boot_disk.name, variableDict)]
            command_dict = {str(c.id): c.dictForJSON() for c in self.commandtemplates}
            for key in command_dict: command_dict[key]["command"] = self._substituteVariables(command_dict[key]["command"], variableDict)  
            result[name] = Instance(name, self.machine_type, self.boot_disk.image, self.location, 
                     self.ex_network, self.ex_tags, self.ex_metadata, dependency_names, 
                     read_disks, read_write_disks, boot_disk, command_dict, 
                     rootdir=self.boot_disk.image.rootdir, preemptible=True, numLocalSSD=0, 
                     localSSDInitSources="", localSSDDests="", gce_manager=gce_manager, log = log)
            
        return result            
        
    @staticmethod
    def findByID(session, iid, user):
        iids=session.query(InstanceTemplate).join(WorkflowTemplate).join(User).filter(InstanceTemplate.id==int(iid)).filter(User.id==user.id).all()
        if len(iids)==0: return None
        else: return iids[0]

    @staticmethod
    def findByName(session, name, user):
        iids=session.query(InstanceTemplate).join(WorkflowTemplate).join(User).filter(InstanceTemplate.name==name).filter(User.id==user.id).all()
        if len(iids)==0: return None
        else: return iids[0]

    @staticmethod
    def delete(session, iid, user):
        inst = InstanceTemplate.findByID(session, iid, user)
        if inst != None:
            session.delete(inst)
            session.commit()
        
#         session.query(InstanceTemplate).filter_by(InstanceTemplate.id==iid).delete()
#         session.query(InstanceTemplate).join(WorkflowTemplate).filter(InstanceTemplate.id==iid).filter(WorkflowTemplate.user_id==user.id).delete()

class CommandTemplateDependencyRelation(orm.Base):
    child_id = Column(Integer, ForeignKey('commandtemplate.id'), primary_key=True)
    parent_id = Column(Integer, ForeignKey('commandtemplate.id'), primary_key=True)

class CommandTemplate(orm.Base):
    '''
    classdocs
    '''
    id = Column(Integer,primary_key=True)
    instance_id = Column(Integer, ForeignKey("instancetemplate.id"))
    instance = relationship(InstanceTemplate, backref = "commandtemplates")
    command_name = Column(String)
    command = Column(String)
    dependencies = relationship("CommandTemplate", secondary='commandtemplatedependencyrelation',
                        primaryjoin=id==CommandTemplateDependencyRelation.parent_id,
                        secondaryjoin=id==CommandTemplateDependencyRelation.child_id,
                        backref="next_commands")

    def __init__(self, instance, command_name, command, dependencies):
        '''
        Constructor
        '''
        self.instance = instance
        self.command_name = command_name
        self.command = command
        self.dependencies = dependencies
        
    def dictForJSON(self):
        return {"id": str(self.id),
              "name": self.command_name,
              "command": self.command,
              "dependencies": [str(d.id) for d in self.dependencies]}
    
    def updateValues(self, instance, command_name, command, dependencies):
        self.instance = instance
        self.command_name = command_name
        self.command = command
        self.dependencies = dependencies
    
    @staticmethod
    def delete(session, cid, user):
        command = CommandTemplate.findByID(session, cid, user)
        if command != None:
            session.delete(command)
            session.commit()
#         session.query(CommandTemplate).join(InstanceTemplate).join(WorkflowTemplate).filter(CommandTemplate.id==cid).filter(WorkflowTemplate.user_id==user.id).delete()
    
    @staticmethod
    def findByID(session, cid, user):
        cids=session.query(CommandTemplate).join(InstanceTemplate).join(WorkflowTemplate).filter(CommandTemplate.id==int(cid)).filter(WorkflowTemplate.user_id==user.id).all()
        if len(cids)==0: return None
        else: return cids[0]
    
    @staticmethod
    def findByName(session, name, user):
        cids=session.query(CommandTemplate).join(InstanceTemplate).join(WorkflowTemplate).filter(CommandTemplate.command_name==name).filter(WorkflowTemplate.user_id==user.id).all()
        if len(cids)==0: return None
        else: return cids[0]



