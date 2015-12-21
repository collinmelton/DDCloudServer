
import os
from sqlalchemy.ext.declarative.api import declared_attr
from pattern.db import primary_key
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import aliased, sessionmaker,relationship,backref, synonym, with_polymorphic, joinedload_all
from sqlalchemy import Column, Integer, String,DateTime,Date, func, Boolean, PickleType, Float, ForeignKeyConstraint
from sqlalchemy import create_engine, func, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey

"""
TODO:
    Refactor utilities for parsing / loading tsv files
"""
    
#------------------------------------------------------------------------------------------------------------#

#Constants and other references

# BASE_DIR = '/Users/jeromeku/Desktop/CODES/' #Should be base project folder
# BASE_DIR = '/Users/cmelton/Documents/AptanaStudio3Workspace/CODES/' #Should be base project folder

BASE_DIR = os.getcwd().split("/DDCloudServer/")[0]+"/DDCloudServer/"
 
DB_NAME = 'laptop_2.db'
DB_DIR = os.path.join(BASE_DIR,'Data')
DB_TYPE = 'sqlite'


#------------------------------------------------------------------------------------------------------------#


#SQLAlchemy set-up, Base ORM Class and Extensions
class TimestampMixin(object):
    created_at = Column(DateTime, default=func.now())

    
class Base(TimestampMixin, object):
    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()
    
    __table_args__ = {'extend_existing': 'True'}


    
#     id = Column(Integer,primary_key=True)
    
#------------------------------------------------------------------------------------------------------------#    
#Helper Functions 
class ORM_Utility(object):
    
    def __init__(self,db_type,db_dir,db_name,echo=False):
        print "db path:", os.path.join(db_dir,db_name)
        self.engine = create_engine(db_type + ":////" + os.path.join(db_dir,db_name),echo=echo, connect_args = {'check_same_thread':False})
#         self.engine = create_engine(db_type + ":///" + db_name,echo=echo)
        self.Base = declarative_base(bind=self.engine,cls=Base)
    
    def loadSession(self):
        session = sessionmaker()
        session.configure(bind=self.engine) 
        self.session = session()
        self.session.autoflush = False
        return self.session
    
    def resetSession(self):
        self.session.close_all()
    
#------------------------------------------------------------------------------------------------------------#    
#Object-Relational Classes and Extensions

class TextReader(object):
    """
    Interface for reading text files
    """

    @classmethod
    def readFile(cls,files,**kwargs):
        raise NotImplementedError

    @classmethod
    def createTableFromFile(cls,**kwargs):
        raise NotImplementedError

#------------------------------------------------------------------------------------------------------------#

def createORMUtility():
    return ORM_Utility(db_type=DB_TYPE,db_dir=DB_DIR,db_name=DB_NAME)

orm = createORMUtility()

 