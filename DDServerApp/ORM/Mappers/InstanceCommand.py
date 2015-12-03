'''
Created on Nov 20, 2015

@author: cmelton
'''

# imports
from DDServerApp.ORM import orm,Column,relationship,String,Integer, PickleType, Float,ForeignKey,backref
from DDServerApp.ORM import Boolean, DateTime
from Instance import Instance

class CommandDependencyRelation(orm.Base):
    child_id = Column(Integer, ForeignKey('instancecommand.id'), primary_key=True)
    parent_id = Column(Integer, ForeignKey('instancecommand.id'), primary_key=True)

class InstanceCommand(orm.Base):
    '''
    This class represents a single command to be run on a single instance.
    '''
    id = Column(Integer,primary_key=True)
    command = Column(String, index=True)
    instance_id = Column(Integer, ForeignKey("instance.id"))
    instance = relationship(Instance, backref=backref('commands'))
    command_dependencies = relationship("InstanceCommand", secondary='commanddependencyrelation',
                            primaryjoin=id==CommandDependencyRelation.parent_id,
                            secondaryjoin=id==CommandDependencyRelation.child_id,
                            backref="parents")
    command_performance_id = Column(Integer, ForeignKey("commandperformance.id"))
    command_performance = relationship("CommandPerformance", backref="command")
    command_type = Column(String)

    def __init__(self, instance, command, command_dependencies, command_type):
        '''
        Constructor
        '''
        self.instance = instance
        self.command = command
        self.command_dependencies = command_dependencies
        self.command_performance = None
        self.command_type = command_type
        
    # adds a performance time point
    def addPerformanceTimePoint(self, name, process_id, user, cpu_percent, memory_percent, rss, vms, read_bytes, write_bytes, time):
        if self.command_performance == None:
            self.command_performance = CommandPerformance(name, process_id, user)
        self.command_performance.addTimePoint(cpu_percent, memory_percent, rss, vms, read_bytes, write_bytes, time)
        
    @staticmethod
    def getOrderedCommandsByInstance(instance):
        def sortByType(ics, type):
            used = [ic for ic in ics if ic.command_dependencies==[] or all([icd.command_type != type for icd in ic.command_dependencies])]
            ics = [ic for ic in ics if ic not in used]
            while ics != []:
                print len(ics), len(used)
                used += [ic for ic in ics if all([icd in used for icd in ic.command_dependencies])]
                ics = [ic for ic in ics if ic not in used]
            return used
        types = set([ic.command_type for ic in instance.commands])
        result = {}
        for t in types:
            result[t] = sortByType([ic for ic in instance.commands if ic.command_type==t], t)
        return result
        

class CommandPerformance(orm.Base):
    '''
    This class tracks performance of a single command run on a single instance.
    '''
    id = Column(Integer,primary_key=True)
    name = Column(String)
    process_id = Column(Integer)
    user = Column(String)
    
    def __init__(self, name, process_id, user):
        '''
        Constructor
        '''
        self.name=name
        self.process_id=process_id
        self.user = user
        
    def addTimePoint(self, cpu_percent, memory_percent, rss, vms, read_bytes, write_bytes, time):
        return CommandPerformance(self, cpu_percent, memory_percent, rss, vms, read_bytes, write_bytes, time)
        
class CommandPerformanceTimePoint(orm.Base):
    '''
    This class tracks the performance of a command at a single instance in time.
    '''
    
    id = Column(Integer,primary_key=True)
    command_performance_id = Column(Integer, ForeignKey("commandperformance.id"))
    command_performance = relationship(CommandPerformance, backref=backref('timepoints'))
    cpu_percent = Column(Float)
    memory_percent = Column(Float)
    rss = Column(Float)
    vms = Column(Float)
    read_bytes = Column(Float)
    write_bytes = Column(Float)
    time = Column(DateTime)
    
    def __init__(self, command_performance, cpu_percent, memory_percent, rss, vms, read_bytes, write_bytes, time):
        '''
        Constructor
        '''
        self.command_performance = command_performance
        self.cpu_percent = float(cpu_percent)
        self.memory_percent = float(memory_percent)
        self.rss = float(rss)
        self.vms = float(vms)
        self.read_bytes = float(read_bytes)
        self.write_bytes = float(write_bytes)
        self.time = time