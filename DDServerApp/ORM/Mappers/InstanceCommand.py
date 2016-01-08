'''
Created on Nov 20, 2015

@author: cmelton
'''

# imports
from DDServerApp.ORM import orm,Column,relationship,String,Integer, PickleType, Float,ForeignKey,backref
from DDServerApp.ORM import Boolean, DateTime
# from DDServerApp.ORM.Mappers import Instance
import pickle, json, subprocess, datetime, time, math, pwd, os, psutil
from threading import Thread, Event



# some global vars
# certain text output for GATK can indicate that the command didn't actually fail even with non zero exit status 
NOT_ACTUALLY_FAILED_LIST=["org.broadinstitute.sting.gatk.CommandLineExecutable.generateGATKRunReport", "org.broadinstitute.gatk.engine.CommandLineExecutable.generateGATKRunReport"]
PERFORMANCE_INTERVAL = 1 # gap between performance checks in secs
UPDATE_SERVER_INTERVAL = int(math.floor(float(max([2, PERFORMANCE_INTERVAL]))/PERFORMANCE_INTERVAL)*PERFORMANCE_INTERVAL) # gap between updating server
VERBOSE = True
#### Some Helper Functions ####

# get the current time
def whatTimeIsIt():
    return datetime.datetime.now()

#### Class Definitions ####

class CommandDependencyRelation(orm.Base):
    child_id = Column(Integer, ForeignKey('instancecommand.id'), primary_key=True)
    parent_id = Column(Integer, ForeignKey('instancecommand.id'), primary_key=True)

class RunCommandThread(Thread):
    '''
    This class will run a parallel thread.
    '''
    
    def __init__(self, command, worker = None):
        Thread.__init__(self)
        self.command = command
        self.worker = worker
        
    def run(self):
        # run command
        self.command.run(worker = self.worker)
        # run the next commands
        newthreads = []
        for next_command in self.command.next_commands:
            if next_command.ready(): 
                newthreads.append(RunCommandThread(next_command, worker = self.worker))
        for thread in newthreads:
            thread.start()
        for thread in newthreads:
            thread.join()

class CheckPerformanceThread(Thread):
    '''
    This class will run a parallel thread to check performance.
    '''
    
    def __init__(self, command, worker = None):
        Thread.__init__(self)
        self.command = command
        self._stop = Event()
        self.worker = worker

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
        
    def run(self):
        while not self.stopped():
            total_wait = 0
            # update performance
            self.command.updatePerformance()
            if total_wait%UPDATE_SERVER_INTERVAL==0: 
                # wait
                total_wait+=PERFORMANCE_INTERVAL
                time.sleep(PERFORMANCE_INTERVAL)
                # update server if its been the right amount of time
                self.command.updateServer(worker = self.worker)
        self.command.updateServer(worker = self.worker)
                 
        
class InstanceCommand(orm.Base):
    '''
    This class represents a single command to be run on a single instance.
    '''
    id = Column(Integer,primary_key=True)
    command = Column(String, index=True)
    instance_id = Column(Integer, ForeignKey("instance.id"))
    instance = relationship("Instance", backref=backref('commands'))
    command_dependencies = relationship("InstanceCommand", secondary='commanddependencyrelation',
                            primaryjoin=id==CommandDependencyRelation.parent_id,
                            secondaryjoin=id==CommandDependencyRelation.child_id,
                            backref="next_commands")
    command_performance_id = Column(Integer, ForeignKey("commandperformance.id"))
    command_performance = relationship("CommandPerformance", backref="command")
    command_type = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    finished = Column(Boolean)
    result = Column(String)
    failed = Column(Boolean)
    process_id = Column(String)

    def __init__(self, instance, command, command_dependencies, command_type, id = None):
        '''
        Constructor
        '''
        self.instance = instance
        self.command = command
        self.command_dependencies = command_dependencies
        self.command_performance = None
        self.command_type = command_type
        self.finished = False
        self.failed = False
        self.result = ""
        self.process_id = 0
        if id != None: self.id = id

    def __str__(self):
        return "< Instance Command: "+self.command[:min(30, len(self.command))]+">"
    
    def __repr__(self):
        return str(self)
    
    @staticmethod
    def getTableNames():
        return [("string", "command", "Command"), 
        ("string", "command_type", "Command Type"),
        ("boolean", "finished", "Finished?"),
        ("boolean", "failed", "Failed?"),
        ("string", "result", "Result")]
    
    def getTableData(self):
        keyvals = [("command", "<a onclick='toggleCommand(\""+str(self.instance.workflows[0].id)+"\", \""+str(self.instance.id)+"\", \""+str(self.id)+"\");'>"+self.command+"</a>"), 
                ("command_type", self.command_type),
                ("finished", self.finished),
                ("failed", self.failed),
                ("result", str(self.result))]
        return {key: {"value": val, "css":""} for key, val in keyvals}
    
    def getPerformanceTableData(self):
        data = [['Time (min)', 'CPU %', 'Memory %', 'Memory (1GB)', 'Write (MB/s)', 'Read (MB/s)']]
        if self.command_performance!=None:
            times = [tp.time for tp in self.command_performance.timepoints]
            if times !=[]:
                mintime = min(times)
                if self.command_performance !=None:
                    for tp in self.command_performance.timepoints:
                        toappend = []
                        toappend.append(float((tp.time-mintime).total_seconds())/60)
                        if tp.cpu_percent!= None: toappend.append(tp.cpu_percent*100)
                        else: toappend.append(0)
                        if tp.memory_percent != None: toappend.append(tp.memory_percent*100)
                        else: toappend.append(0)
                        if float(tp.rss)!=None: toappend.append(float(tp.rss)/1000000)
                        else: toappend.append(0)
                        if tp.read_bytes!=None: toappend.append(float(tp.read_bytes)/1000000)
                        else: toappend.append(0)
                        if tp.write_bytes!=None: toappend.append(float(tp.write_bytes)/1000000)
                        else: toappend.append(0)
                        data.append(toappend)
        else: data.append([0,0,0,0,0,0])
        return data
                
#     tp.cpu_percent
#     tp.memory_percent = Column(Float)
#     tp.rss = Column(Float)
#     vms = Column(Float)
#     read_bytes = Column(Float)
#     write_bytes = Column(Float)
#     time = Column(DateTime)
            
#         ['1',  100,      1, 10, 1],
#         ['2',  15,      34, 10, 1],
#         ['3',  50,       55, 10, 1],
#         ['4',  5,      40, 10, 1]]
    
    def updateServer(self, worker = None):
        '''
        Updates the server with command performance data.
        '''
        data = self.getCommandData()
        if worker != None:
            worker.updateCommandData(data)
        if VERBOSE: print "updating server"
    
    # method to determine if command is ready to run
    def ready(self):
        '''
        Determines if the command is ready (i.e. its dependencies finished without error).
        '''
        return all([(cd.finished and not cd.failed) for cd in self.command_dependencies])
        
    def getStatus(self):
        '''
        Returns the status of the command (failed, complete, not finished).
        '''
        if self.finished: 
            if self.failed: return "failed"
            else: return "complete"
        else: return "not finished" 

    # run the command if not already run and finished
    def run(self, worker = None):
        if VERBOSE: print "starting thread", self.command
        # set start time
        self.start_time=whatTimeIsIt()
        # start command
        running_subprocess = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # get command process id
        self.process_id = running_subprocess.pid
        # use process id to monitor performance
        perf_thread = CheckPerformanceThread(self, worker = worker)
        perf_thread.start()
        # wait for process to finish
        running_subprocess.wait()
        self.result = running_subprocess.stdout.read()
        if VERBOSE: 
            print "COMMAND:", self.command
            print "RESULT:", self.result
        error = running_subprocess.stderr.read()
        return_code = running_subprocess.returncode
        # stop the performance thread
        perf_thread.stop()
        perf_thread.join()
        # handle errors
        if return_code != 0:
            self.failed = True
            self.result = "\n".join(map(str, [error, self.result]))
            # make sure failure isn't a false alarm
            notfailed=False
            for item in NOT_ACTUALLY_FAILED_LIST:
                if item in self.result:
                    notfailed=True
            if notfailed:
                self.failed=False
        # set end time
        self.end_time=whatTimeIsIt()
        self.finished = True
        self.updateServer(worker = worker)
        return self.failed    
        
    def updatePerformance(self):
        if VERBOSE: print "updating performance"
        self.addPerformanceTimePoint(self.process_id)
        
    # adds a performance time point
    def addPerformanceTimePoint(self, process_id):
        # get process data
        try: 
            process = psutil.Process(process_id)
        except: 
            # return false if it didn't work
            return False
        # get performance data
        try: cpu_percent = process.cpu_percent(interval=0.1)
        except: cpu_percent = None
        try: memory_percent = process.memory_percent()
        except: memory_percent = None
        try: rss = process.memory_info().__dict__["rss"]
        except: rss = None
        try: vms = process.memory_info().__dict__["vms"]
        except: vms = None
        try: read_bytes = process.io_counters().__dict__["read_bytes"]
        except: read_bytes = None
        try: write_bytes = process.io_counters().__dict__["write_bytes"]
        except: write_bytes = None
        time = whatTimeIsIt()
        # add data
        if self.command_performance == None:
            self.command_performance = CommandPerformance(process_id)
        if not any([x == None for x in [cpu_percent, memory_percent]]):
            self.command_performance.addTimePoint(cpu_percent, memory_percent, rss, vms, read_bytes, write_bytes, time)
        # return True if it worked
        return True
    
    # method to pickle import instance info
    def toSummary(self):
        '''
        Returns a summary dictionary basic command info. This is used to send command data
        from master to worker.
        '''
        return {"id": self.id,
                "command": self.command,
                "command_dependencies": [c.id for c in self.command_dependencies],
                "command_type": self.command_type,
                "id": self.id
                }
    
    # returns serialized (string) version of performance data
    def getCommandData(self):
        '''
        Returns a json string representing command performance.
        '''
        result = {}
        if self.command_performance != None:
            result["performance_update"] = self.command_performance.getTimePointsSummary()
        else:
            result["performance_update"] = []
        result["finished"] = self.finished
        result["failed"] = self.failed
        result["result"] = self.result
        result['start_time'] = self.start_time
        result['end_time'] = self.end_time
        if self.command_performance!=None:
            result["process_id"] = self.command_performance.process_id
        else:
            result["process_id"] = None
        result["id"] = self.id
        return result
    
    # updates command with command data from worker
    def updateCommandData(self, data):
        '''
        Updates command status and adds performance data.
        '''
        if VERBOSE: print "UPDATING COMMAND DATA!!!", self.command
        if VERBOSE: print data["start_time"]
        if type(data["start_time"]) == float:
            data["start_time"] = datetime.datetime.fromtimestamp(data["start_time"])
        self.start_time = data["start_time"]
        if VERBOSE: print data["end_time"]
        if type(data["end_time"]) == float:
            data["end_time"] = datetime.datetime.fromtimestamp(data["end_time"])
            self.end_time = data["end_time"]
        if VERBOSE: print data["finished"]
        self.finished = (data["finished"] or self.finished)
        if VERBOSE: print data["failed"]
        self.failed = (data["failed"] or self.failed)
        if VERBOSE: print data["result"]
        if data["result"]!="": self.result = data["result"]
        if VERBOSE: print "updating command performance"
        if VERBOSE: print data["process_id"]
        if self.command_performance == None:
            self.command_performance = CommandPerformance(data["process_id"])
        if VERBOSE: print "command okay"
        if VERBOSE: print data["performance_update"]
        self.command_performance.updatePerformanceData(data["performance_update"])
    
    @staticmethod
    def getOrderedCommandsByInstance(instance):
        def sortByType(ics, type):
            used = [ic for ic in ics if ic.command_dependencies==[] or all([icd.command_type != type for icd in ic.command_dependencies])]
            ics = [ic for ic in ics if ic not in used]
            while ics != []:
                if VERBOSE: print len(ics), len(used)
                used += [ic for ic in ics if all([icd in used for icd in ic.command_dependencies])]
                ics = [ic for ic in ics if ic not in used]
            return used
        types = set([ic.command_type for ic in instance.commands])
        result = {}
        for t in types:
            result[t] = sortByType([ic for ic in instance.commands if ic.command_type==t], t)
        return result
    
    @staticmethod
    def generateCommandFromDict(data, command_dependencies = []):
        '''
        This method returns bare bones InstanceCommand from pickled data.
        '''
        return InstanceCommand(None, data["command"], command_dependencies, data["command_type"], id=data["id"])
    
#     @staticmethod
#     def generateJSONFromCommands(commands):
#         return {command.id: command.toSummary() for command in commands}
    
    @staticmethod
    def generateCommandsFromJSON(json_string):
        '''
        This method will generate a list of the commands 
        given a json object with command info.
        '''
        if VERBOSE: print json_string
        data = json.loads(json_string)
        commands = {int(key): {"command": InstanceCommand.generateCommandFromDict(data[key]), 
                          "dependencies": data[key]["command_dependencies"]} for key in data}
        for key in commands:
            commands[key]["command"].command_dependencies = [commands[dkey]["command"] for dkey in commands[key]["dependencies"]]
        return [val["command"] for val in commands.values()]
    
    @staticmethod
    def getFirstCommands(commands):
        '''
        Returns a list of the first commands to run given dependencies in commands.
        '''
        return [command for command in commands if all([cd not in commands for cd in command.command_dependencies])]

    @staticmethod
    def findByCommand(session, command, user):
        from DDServerApp.ORM.Mappers.Workflow import Workflow, Instance, InstanceWorkflowLink
        iids=session.query(InstanceCommand).join(Instance).join(InstanceWorkflowLink).join(Workflow).filter(InstanceCommand.command==command).filter(Workflow.user_id==user.id).all()
        if len(iids)==0: return None
        else: return iids[0]  

class CommandPerformance(orm.Base):
    '''
    This class tracks performance of a single command run on a single instance.
    '''
    id = Column(Integer,primary_key=True)
    process_id = Column(Integer)
    user = Column(String)
    
    def __init__(self, process_id):
        '''
        Constructor
        '''
        self.process_id=process_id
        self.user = pwd.getpwuid(os.getuid())[0]
        
    def addTimePoint(self, cpu_percent, memory_percent, rss, vms, read_bytes, write_bytes, time):
        return CommandPerformanceTimePoint(self, cpu_percent, memory_percent, rss, vms, read_bytes, write_bytes, time)
    
    def updatePerformanceData(self, data):
        '''
        Adds time point data to command performance.
        '''
        for tp_data in data:
            if VERBOSE: print "command performance, updating time point data", tp_data
            CommandPerformanceTimePoint.fromSummaryDict(tp_data, self)
    
    # returns serialized (string) version of performance data
    def getTimePointsSummary(self, all = False):
        '''
        Returns a json string representing command performance.
        '''
        if not all: timepoints = [tp for tp in self.timepoints if not tp.sentToServer]
        else: timepoints = self.timepoints
        data = [tp.summaryDict() for tp in timepoints]
        return data
        
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
    sentToServer = Column(Boolean)
    
    def __init__(self, command_performance, cpu_percent, memory_percent, rss, vms, read_bytes, write_bytes, time):
        '''
        Constructor
        '''
        self.command_performance = command_performance
#         if VERBOSE: print cpu_percent
        self.cpu_percent = float(cpu_percent)
#         if VERBOSE: print memory_percent
        self.memory_percent = float(memory_percent)
#         if VERBOSE: print rss
        self.rss = float(rss)
#         if VERBOSE: print vms
        self.vms = float(vms)
#         if VERBOSE: print read_bytes
        self.read_bytes = read_bytes
#         if VERBOSE: print write_bytes
        self.write_bytes = write_bytes
        if VERBOSE: print "time", time, type(time)
        if type(time) == float:
            self.time = datetime.datetime.fromtimestamp(time)
            if VERBOSE: print self.time
        else:
            self.time = time
        self.sentToServer = False
        
    def summaryDict(self):
        '''
        Serializes important time point info.
        '''
        self.sentToServer = True
        return {"cpu_percent": self.cpu_percent,
                             "memory_percent": self.memory_percent,
                             "rss": self.rss,
                             "vms": self.vms,
                             "read_bytes": self.read_bytes,
                             "write_bytes": self.write_bytes,
                             "time": self.time}
        
    @staticmethod
    def fromSummaryDict(data, command_performance):
        '''
        Creates instance given pickled data.
        '''
        return CommandPerformanceTimePoint(command_performance, data["cpu_percent"], data["memory_percent"], 
                                           data["rss"], data["vms"], data["read_bytes"], data["write_bytes"], 
                                           data["time"])