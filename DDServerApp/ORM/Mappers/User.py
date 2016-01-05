'''
Created on Jul 24, 2014

@author: cmelton
'''

from DDServerApp.ORM import orm,Column,relationship,String,Integer,ForeignKey,backref, with_polymorphic
from werkzeug.security import generate_password_hash, check_password_hash
from Instance import Instance
from Disk import Disk
#------------------------------------------------------------------------------------------------------------#

#Constants and other references


#------------------------------------------------------------------------------------------------------------#

#Utilities for handling I/O and functions across all cancer-related objects
class UserUtilities():
    """
    Singleton object that performs utility functions across all Cancer and related objects
    """    
        
    @staticmethod
    def addAllToDB(session):
        session.add_all(User.getUsers())
        session.commit()

#------------------------------------------------------------------------------------------------------------#

# ORM Classes

class InstancePermissions(orm.Base):
    instance_id = Column(Integer, ForeignKey('instance.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
     
class DiskPermissions(orm.Base):
    disk_id = Column(Integer, ForeignKey('disk.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

class User(orm.Base):
    '''
    Object-Relation for a user with a name and a role.
    '''

    __users = set()
    
    id = Column(Integer,primary_key=True)
    name = Column(String, unique=True, index=True)
    role = Column(String)
    instances = relationship(Instance, secondary='instancepermissions', backref = 'user')
    disks = relationship(Disk, secondary='diskpermissions', backref = 'user')
    pw_hash = Column(String)

    def __init__(self, name, role, password):
        '''
        Constructor
        '''
        self.name=name
        self.role=role
        User.__users.add(self)
        self.set_password(password)
        self.instances = []
        self.disks = []
    
    def addDisks(self, disks):
        self.disks = self.disks + disks
        
    def addInstances(self, instances):
        self.instances+=instances
        

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def adminGetUsers(self, session):
        if "admin" in self.role:
            return map(lambda u: u.name, User.getUsers(session=session))
        else: return ["none"]

    def getUserData(self):
        workflowData = {wf.id: wf.dictForJSON() for wf in self.workflowtemplates}
        imageData = {im.id: im.dictForJSON() for im in self.images}
        if self.credentials != None:
            credentialData = {cred.id: cred.dictForJSON() for cred in self.credentials}
        else: 
            credentialData = {}
        return {"workflows": workflowData, 
                "images": imageData,
                "credentials": credentialData,
                "active_workflows":self.getActiveWorkflows()}
        
    def getActiveWorkflows(self):
        return {wft.id: wft.dictForJSON() for wft in self.workflowtemplates if any([wf.active for wf in wft.workflows])}
        
    @staticmethod
    def newUser(username, role, password, session):
        if User.findUser(username, session)==None:
            newuser = User(username, role, password)
            session.add_all([newuser])
            session.commit()
        else:
            newuser = None
        return newuser 

    @staticmethod
    def findUser(name, session):
        """
        """
        users=session.query(User).filter(User.name==name).all()
        if len(users)==0: return None
        else: return users[0]

    @staticmethod
    def login(name, password, session):
        user = User.findUser(name, session)
        if user == None: return "Invalid User"
        if user.check_password(password): return user
        else: return "Invalid Password"
        
    @staticmethod
    def getUsers(session = None):
        """
        Returns current list of user objects
        """
        if session == None: return User.__users
        else: return session.query(User).all()
             


