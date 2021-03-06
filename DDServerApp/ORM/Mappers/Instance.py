'''
Created on Nov 20, 2015

@author: cmelton
'''

# imports
from DDServerApp.ORM import orm,Column,relationship,String,Integer, PickleType, Float,ForeignKey,backref,TextReader, joinedload_all
from DDServerApp.ORM import BASE_DIR, Boolean
from DDServerApp.ORM.Mappers import InstanceCommand#, GCEManagerBinding, LogFile
import sys, time
from Disk import Disk

VERBOSE = True

class InstanceDependencyRelation(orm.Base):
    '''
    This relation maps many instances to many instances. 
    '''
    child_id = Column(Integer, ForeignKey('instance.id'), primary_key=True)
    parent_id = Column(Integer, ForeignKey('instance.id'), primary_key=True)

class ReadDiskInstanceLink(orm.Base):
    '''
    This relation maps many disks to many instances.
    '''
    disk_id = Column(Integer, ForeignKey('disk.id'), primary_key=True)
    instance_id = Column(Integer, ForeignKey('instance.id'), primary_key=True)
    
class ReadWriteDiskInstanceLink(orm.Base):
    '''
    This relation maps many disks to many instances.
    '''
    disk_id = Column(Integer, ForeignKey('disk.id'), primary_key=True)
    instance_id = Column(Integer, ForeignKey('instance.id'), primary_key=True)

class Instance(orm.Base):
    '''
    This class represents an instance to be run on the Google Compute Engine.
    '''
    id = Column(Integer,primary_key=True)
    name = Column(String, index=True)
    dependency_names = Column(PickleType)
    dependencies = relationship("Instance", secondary='instancedependencyrelation',
                        primaryjoin=id==InstanceDependencyRelation.parent_id,
                        secondaryjoin=id==InstanceDependencyRelation.child_id,
                        backref="next_instances")
    node_params = Column(PickleType)
    read_disks = relationship(Disk, secondary='readdiskinstancelink')
    read_write_disks = relationship(Disk, secondary='readwritediskinstancelink')
    boot_disk_id = Column(Integer, ForeignKey("disk.id"))
    boot_disk = relationship(Disk)
    created = Column(Boolean)
    destroyed = Column(Boolean)
    failed = Column(Boolean)
    status = Column(String)
    rootdir = Column(String)
    ssh_error_counter = Column(Integer)
    preemptible = Column(Boolean)
    numLocalSSD = Column(Integer)
    localSSDInitSources = Column(PickleType)
    localSSDDests = Column(PickleType)
    command_dict = Column(PickleType)
    machine_type = Column(String)
    image_name = Column(String)
    location = Column(String)
    network = Column(String)
    tagString = Column(String)
    metadataString = Column(String)
    image_id = Column(Integer, ForeignKey("image.id"))
    image = relationship("Image", backref = "instances")
    gce_manager_id = Column(Integer, ForeignKey("gcemanagerbinding.id"))
    gce_manager = relationship("GCEManagerBinding", backref = "instances")
    log_id = Column(Integer, ForeignKey("logfile.id"))
    log = relationship("LogFile", backref = "instances")

    def __init__(self, name, machine_type, image, location, network, tagString,
                 metadataString, dependency_names, read_disks, read_write_disks, 
                 boot_disk, command_dict, rootdir="/home/cmelton/", preemptible=True, numLocalSSD=0, 
                 localSSDInitSources="", localSSDDests="", gce_manager=None, log = None):
        '''
        Constructor
        '''
        self.name=name
        self.dependency_names=dependency_names
        self.dependencies = []
        self.read_disks=read_disks
        self.read_write_disks=read_write_disks
        self.boot_disk=boot_disk
        self.created=False
        self.destroyed=False
        self.node=None
        self.failed=False
        self.status="not started"
        self.rootdir=rootdir
        self.ssh_error_counter = 0
        self.preemptible = preemptible
        self.numLocalSSD = numLocalSSD
        self.localSSDInitSources = localSSDInitSources
        self.localSSDDests = localSSDDests
        self.command_dict = command_dict
        self.machine_type = machine_type
        self.image = image
        self.location = location
        self.network = network
        self.tagString = tagString
        self.metadataString = metadataString
        self.buildNodeParams(machine_type, image.name, location, network, tagString, metadataString)
        self.gce_manager = gce_manager
        self.log = log
        self.printToLog("initialized instance class")
        # moving to on instance creation to allow disk formatting to be done properly #self._initCommands()
    
    # client key and secret are unique to each instance, the access token and secret are unique
    # for each client, these 4 values ensure that a particular instance is getting access to the 
    # correct instance commands and sending back performance data associated with these commands 
    
    @staticmethod
    def getTableNames():
        return [("string", "name", "Name"), 
        ("string", "status", "Status"),
        ("boolean", "preemptible", "Preemptible"),
        ("string", "machine_type", "Machine Type"),
        ("string", "location", "Location")]
    
    def getTableData(self):
        {"key1": {"value":"<a onclick='toggleCommand(\"1\");'>Command 1</a>", "css":""},
                       "key2": {"value":"result 1", "css":""}}
        keyvals = [("name", "<a onclick='toggleCommands(\""+str(self.workflows[0].id)+"\", \""+str(self.id)+"\");'>"+self.name+"</a>"), 
                ("status", self.status),
                ("preemptible", self.preemptible),
                ("machine_type", self.machine_type),
                ("location", self.location)]
        return {key: {"value": val, "css":""} for key, val in keyvals}

    def _getClientAndAccessTokens(self, session):
        from Oauth import Client
        if VERBOSE: print self.client
        if self.client == []:
            client = Client(self.name, "instance client", self.workflows[0].user, ["full"], [], self)
            session.add(client)
            session.commit()
        else: 
            client = self.client[0]
        if VERBOSE: print "client.accesstoken", client.accesstoken
        if client.accesstoken == []:
            accesstoken = client.createAccessToken(session)
            session.add(accesstoken)
            session.commit()
        else:
            accesstoken = client.accesstoken[0]
        return client.client_key, client.client_secret, accesstoken.token, accesstoken.secret        
    
    def _initCommands(self):
        allCommands = []
        # parse startup commands
        startup_commands = "\n".join([self._mountDisksScript(), self._setActiveGcloudAuthAccount(), 
                                      self._initialize_disks()]).split("\n")
        startup_commands = [c for c in startup_commands if c!=""]                                      
        # add startup commands
        startup_commands = self.addCommandSequence(startup_commands, "startup", [])
        # parse and add commands
        commands = self.parseCommandDict(startupCommands=startup_commands)
        # parse commands 
        shutdown_commands = (self._save_disk_content()+"\n"+self._unmountDisksScript()).split("\n")
        shutdown_commands = [c for c in shutdown_commands if c!=""]
        # add commands
        shutdown_commands = self.addCommandSequence(shutdown_commands, "shutdown", commands)
        
        return {"startup":startup_commands, 
                "main":commands, 
                "shutdown":shutdown_commands}
    
    # code to run (on actual instance after boot) to initialize read/write disks, will copy disks contents to disk from some source
    def _initialize_disks(self):
        result = "\n".join([d.initialization_script() for d in self.read_write_disks])
        for i in range(min(self.numLocalSSD, len(self.localSSDInitSources))):
            source = self.localSSDInitSources[i]
            if source != "":
                result += "\n"+"gsutil rsync -r "+source+" /mnt/lssd-"+str(i)
        return result

    # code to run (on actual instance after boot) to save disk content 
    def _save_disk_content(self):
        # save disk content
        result="\n".join(map(lambda disk: disk.contentSave("/usr/local/bin/python2.7 "+self.rootdir+"DDCloudServer/DDServerApp/Utilities/writeDiskContentFile.py"), self.read_write_disks))
        # save disk files to other location (e.g. cloud storage)
        result += "\n".join([d.shutdown_save_script() for d in self.read_write_disks])
        for i in range(min(self.numLocalSSD, len(self.localSSDDests))):
            dest = self.localSSDDests[i]
            if dest != "":
                result += "\n"+"gsutil rsync -r /mnt/lssd-"+str(i)+ " "+dest
        return result

    # code to run (on actual instance after boot) to mount local ssd drives
    def _mount_local_ssd(self):
        return ["mkdir -p  /mnt/lssd-"+str(i)+ "\n /usr/share/google/safe_format_and_mount -m 'mkfs.ext4 -F' /dev/disk/by-id/scsi-"+str(i)+"Google_EphemeralDisk_local-ssd-"+str(i)+" /mnt/lssd-"+str(i) for i in range(self.numLocalSSD)]
    
    # code to run (on actual instance after boot) to mount disks
    def _mountDisksScript(self):
        read_only=map(lambda disk: disk.mount_script(False), self.read_disks)
        read_write=map(lambda disk: disk.mount_script(True), self.read_write_disks)
        local_ssd=self._mount_local_ssd()
        read_write_disk_restore = map(lambda disk: disk.contentRestore("/usr/local/bin/python2.7 "+self.rootdir+"DDCloudServer/DDServerApp/Utilities/restoreDiskContent.py"), self.read_write_disks)
        result= "\n".join(read_only+read_write+local_ssd+read_write_disk_restore)
        return result
    
    # code to run (on actual instance after boot) to unmount disks
    def _unmountDisksScript(self):
        read_only=map(lambda disk: disk.unmount_script(), self.read_disks)
        read_write=map(lambda disk: disk.unmount_script(), self.read_write_disks)
        result= "\n".join(read_only+read_write)
        return result
    
    # code to run (on actual instance after boot) to set the active gcloud account
    def _setActiveGcloudAuthAccount(self):
        return "/usr/local/bin/gcloud config set account "+self.image.authAccount    
    
    def addCommandSequence(self, command_list, command_type, command_dependencies = [], session=None):
        from InstanceCommand import InstanceCommand
        new_commands = []
        for command in command_list:
            new_command = InstanceCommand(self, command, command_dependencies, command_type)
            new_commands.append(new_command)
            command_dependencies = [new_command]
        if session != None:
            session.add_all(new_commands)
            session.commit()
        return new_commands 

    def parseCommandDict(self, startupCommands=[]):
        print "PARSING COMMAND DICTIONARY!!!"
        from InstanceCommand import InstanceCommand
        newCommands = {}
        # make commands
        print self.command_dict
        for id in self.command_dict:
            newCommands[id] = []
            deps = startupCommands # the first command in all command sequences get startup commands as dependencies
            for line in self.command_dict[id]["command"].split("\n"):
                line = line.strip()
                if line!="": 
                    newCommand = InstanceCommand(self, line, deps, "main")
                    newCommands[id].append(newCommand)
                    deps = [newCommand]
        print newCommands.keys()
        for key in newCommands.keys():
            print "KEY:", key, newCommands[key] 
#         print newCommands.values()
        # set dependencies
        for id in newCommands:
            deps = []
#             deps = startupCommands
            for newCommand in newCommands[id]:
                for did in self.command_dict[id]["dependencies"]: 
                    deps += newCommands[did]
                    print newCommand, "adding command deps", newCommands[did]
#                 newCommand.dependencies = [newCommands[did] for did in self.command_dict[id]["dependencies"]]+startupCommands
                newCommand.command_dependencies = list(set(newCommand.command_dependencies+deps))
        result = []
        for commandList in newCommands.values():
            result += commandList
        return result


    def buildNodeParams(self, machine_type, image_name, location, network, tags, metadata):
        node_params={}
        for param, val in [("size", machine_type), ("image", image_name), ("location", location),
                           ("ex_network", network)]:
            node_params[param]=val
        if node_params["ex_network"]=="": node_params["ex_network"] = "default"
        # parse ex_tags
        if tags == "":
            node_params["ex_tags"]=[] 
        else: 
            node_params["ex_tags"]=tags.split("|")
        # parse ex_metadata and add to node params
        node_params["ex_metadata"]={'items': []}
        for pair in metadata.split("|"):
            if pair!="" and ":" in pair:
                key, value= pair.split(":", 1)
                node_params["ex_metadata"]["items"].append({"key":key, "value":value})
        self.node_params = node_params
                  

    # generates a list of commands from the command dictionary input

    # given a dictionary of instances set dependencies using dependency_names
    def setDependencies(self, instanceDict):
        for name in self.dependency_names:
            if name in instanceDict:
                self.dependencies.append(instanceDict[name])
            else:
                self.printToLog("dependency name"+ name+ "wasn't found!!")

    # adds myDriver, instance, and log to instance
    def reinit(self, myDriver, log):
#         self.gce_manager = myDriver
#         self.log = log
        # if already created and not destroyed update the instance to see if it is still present on gce
        if self.created and not self.destroyed: self.updateNode()

    # string output
    def __str__(self):
        return "instance object: "+self.name
    
    # representation output
    def __repr__(self):
        return str(self)

    # function to print text to the log file
    def printToLog(self, text):
#         if "log" in self.__dict__ and self.log!=None:
        output=self.name+"\t"+text
        self.log.write(output)

    # returns text with the header and values in tab delimitted format 
    def toString(self):
        tabDelim=self.tabDelimSummary()
        return("\n".join([tabDelim["header"],tabDelim["values"]]))

    # update command data, this is built for data coming from a worker instance
    def updateCommandData(self, data, session):
        thiscommand = next(c for c in self.commands if c.id == data["id"])
        thiscommand.updateCommandData(data)
        session.add(thiscommand)
        session.commit()
        self.printToLog("updated command data")

    # restarting instance by destroying and recreating
    def manual_restart(self, session):
        self.printToLog("performing manual restart")
        self.destroy(instances=None, destroydisks=False, force = False)
        for node in self.gce_manager.list_nodes():
            self.printToLog(str(node.__dict__)) 
        self.create(session, restart=True)
    
    # in theory try to reboot node without destroying but so far that isn't working 
    # so for now just destroy node then create again
    def restart(self, session):
        self.failed = any([c.failed for c in self.commands])
        if self.failed: self.status = "errored"
        if not self.failed and all([c.finished for c in self.commands]):
            self.status = "completed"
            return self.finish(session)
        else:
            result = self.updateNode()
            if result == None:
                self.manual_restart(session)
            self.printToLog("recreated instance on GCE")
            self.created=True
            self.failed=False
            self.destroyed=False
            self.status="started"
            return {"restarted": True}

    # return boolean to indicate if instance has been started
    def started(self):
        return self.created
    
    # check to see if dependencies (instances required to complete before this one can start) have completed
    def __dependenciesReady(self):
        for d in self.dependencies:
            if not d.status=="completed":
                self.printToLog(str(d)+" not ready")
                return False
        return True

    # check if instance is ready and if yes start job
    def startIfReady(self, session):
#         session.add(self)
#         session.commit()
#         for command in self.commands:
#             print command.id, command.command_type, [c.id for c in command.command_dependencies]
# 
#         return False
        
        # make sure if created it is either failed or completed or an active instance
        if self.created and not self.failed and self.status !="completed":
            node = self.updateNode()
            if node == None: 
                # set created to false
                self.created = False
                # reset commands by deleting old and making new
                print "command status", [c.finished for c in self.commands]
                for c in self.commands: session.delete(c)
                self._initCommands()
                session.add(self)
                session.commit()
                print "command status", [c.finished for c in self.commands]
        
                self.printToLog("starting if ready instance "+self.name)
        # if already run do nothing
        if self.status=="completed": 
            print "status is", self.status
            return False
        # if dependencies not ready do nothing
        if not self.__dependenciesReady(): 
            print "dependencies not ready"
            return False
        # if not created create and not failed its ready so create
        if not self.created and not self.failed:
            self._initCommands()
            self.create(session)
            return True
        print "nothing else to do", self.created, self.failed
        # if failed or other do nothing
        return False

    # finish and start new instances if ready
    def finish(self, session):
        self.failed = any([c.failed for c in self.commands])
        if self.failed: self.status = "errored"
        if not self.failed and all([c.finished for c in self.commands]):
            self.status = "completed"
        print "status:", self.status
        session.add(self)
        session.commit()
        result = {}
        if self.status == "completed":
            self.destroy(instances=self.workflows[0].instances, destroydisks=True, force = False)
            for instance in self.next_instances:
                print "checking if ready", instance.name
                result[instance.name]=instance.startIfReady(session)
            for disk in self.read_disks:
                disk.destroyifnotneeded(self.workflows[0].instances)
            for disk in self.read_write_disks:
                disk.destroyifnotneeded(self.workflows[0].instances)
            self.workflows[0].checkIfFinished()
        session.add(self)
        session.commit()
        print "finishing result", result
        return result

    # given list of instances/nodes set node attribute if has the same name
    def setInstances(self, nodes):
        for node in nodes:
            if node.name==self.name:
                self.node=node
                self.created=True
                self.failed=False
                self.destroyed=False
                self.status="started"
                self.log.write(self.name+"is already created!!")   
    
#     # package script in python script shell
#     # the StartupWrapper.py program executes the script, saves the output to google cloud storage and updates the project meta data on start and completion
    def packageScript(self, session):          
        clientKey, clientSecret, tokenKey, tokenSecret = self._getClientAndAccessTokens(session)
        address = self.workflows[0].address
        result = "\n/usr/local/bin/python2.7 "+self.rootdir+"DDCloudServer/DDServerApp/Utilities/Worker.py --TK \""+tokenKey+"\" --TS \""+tokenSecret+"\" --CK "+clientKey+" --CS "+clientSecret + " --AD "+address + " > startupScriptOutput.txt"
        if VERBOSE: print result
        return result
# /DDServerApp/Utilities/Worker.py
#     def packageScriptNew(self):
#         script = self._mountDisksScript()+"\n"+self._setActiveGcloudAuthAccount()+"\n"+self._initialize_disks()+"\n"+self.script+"\n"+self._save_disk_content()
#         shutdownscript = self._unmountDisksScript()
#         result = "\n#! /bin/bash"
#         if self.activateStackdriver: result += "\nsudo bash stack-install.sh --api-key="+self.StackdriverAPIKey
#         result += "\n/usr/local/bin/python2.7 "+self.rootdir+"DynamicDiskCloudSoftware/Worker/Startup.py --S \""+script.replace("\'", "'")+"\" --SD \""+shutdownscript.replace("\'", "'")+"\" --H "+self.rootdir+"StartupCommandHistoryv3.pickle --N "+self.name
#         return(result)


    
    # create and run node on GCE
    def create(self, session, restart = False):
        if not self.created: 
#             print self.packageScript(session)
#             return 
            #raise Exception('Trying to create already created instance on '+self.name)
            # make sure all necessary disks are created
#             read_disks = []
            for disk in self.read_disks:
                if not disk.created:
                    disk.create()
#                     read_disks.append(disk.create())
#                 else:
#                     read_disks.append(disk.updateDisk())
#             read_write_disks = []
            for disk in self.read_write_disks:
                if not disk.created:
                    disk.create()
#                     read_write_disks.append(disk.create())
#                 else:
#                     read_write_disks.append(disk.updateDisk())
            
            # if boot disk exists delete and make new
            if self.boot_disk.updateDisk() != None:
                self.boot_disk.destroy()
            boot_disk = self.boot_disk.create()
            self.boot_disk.formatted=True # make sure to indicate that it is formatted because a boot disk will be formatted on startup
                
            # add startup script to metadata and make sure drive mounting is added to startup script
            if not restart:
                if VERBOSE: print "before", self.node_params["ex_metadata"]["items"]
                if VERBOSE: print "adding", {"key":"startup-script", "value":self.packageScript(session)}
                self.node_params["ex_metadata"]["items"].append({"key":"startup-script", "value":self.packageScript(session)})
                self.node_params["ex_metadata"]["items"].append({"key":"shutdown-script", "value":self.packageShutdownScript(session)})
                if VERBOSE: print "after", self.node_params["ex_metadata"]["items"]

            # change mode of disks and prepare them in a list for node creation
            print "setting read disks"
            for disk in self.read_disks:
                disk.mode="READ_ONLY"
#                 session.add(disk)
#                 session.commit()
#                 print disk.name, disk.mode
            print "setting read/write disks"
            for disk in self.read_write_disks:
                disk.mode="READ_WRITE"
#                 session.add(disk)
#                 session.commit()
#                 print disk.name, disk.mode
            additionalDisks=self.read_disks+self.read_write_disks
            print "additional disks"
            if VERBOSE: print additionalDisks
            for d in additionalDisks:
                print d.name, d.mode
            additionalDisks = list(set(additionalDisks))
            print "additional disks after removing dups"
            for d in additionalDisks:
                print d.name, d.mode
            if VERBOSE: print additionalDisks
            
            # create node = GCE instance
            i=0
            node = None
            while node==None:
                i+=1
                if VERBOSE: print self.name, self.node_params["size"], self.node_params["image"], self.node_params["location"]
                if VERBOSE: print self.node_params["ex_network"], self.node_params["ex_tags"], self.node_params["ex_metadata"]
                if VERBOSE: print boot_disk
                if VERBOSE: print additionalDisks, self.preemptible, self.numLocalSSD, self.log
#                 self.gce_manager.create_node(self.name, self.node_params["size"], self.node_params["image"], location=self.node_params["location"],
#                                       ex_network=self.node_params["ex_network"], ex_tags=self.node_params["ex_tags"], ex_metadata=self.node_params["ex_metadata"], 
#                                       ex_boot_disk=boot_disk, serviceAccountScopes=["https://www.googleapis.com/auth/compute", "https://www.googleapis.com/auth/devstorage.read_write"], 
#                                       additionalDisks=additionalDisks, preemptible=self.preemptible, numLocalSSD=self.numLocalSSD, log=self.log)
                 
                node=self.trycommand(self.gce_manager.create_node, self.name, self.node_params["size"], self.node_params["image"], location=self.node_params["location"],
                                      ex_network=self.node_params["ex_network"], ex_tags=self.node_params["ex_tags"], ex_metadata=self.node_params["ex_metadata"], 
                                      ex_boot_disk=boot_disk, serviceAccountScopes=["https://www.googleapis.com/auth/compute", "https://www.googleapis.com/auth/devstorage.read_write"], 
                                      additionalDisks=additionalDisks, preemptible=self.preemptible, numLocalSSD=self.numLocalSSD, log=self.log)
                if node==None:
                    node=self.trycommand(self.gce_manager.ex_get_node, self.name)
                if i==2:
                    self.printToLog("failed to create instance on GCE")
                    break
                self.node = node
            self.printToLog("created instance on GCE")
            self.created=True
            self.failed=False
            self.destroyed=False
            self.status="started"
        else: self.printToLog("instance already created on GCE")
        session.add(self)
        session.commit()
    
    # update and return node by checking if it exists on GCE
    def updateNode(self):
        print self.__dict__.keys()
        if "node" not in self.__dict__ or self.node == None: 
            print "getting node"
#             node = self.gce_manager.ex_get_node(self.name)
            node=self.trycommand(self.gce_manager.ex_get_node, self.name)
        else: 
            if "node" in self.__dict__ and self.node !=None: node = self.node
            else: node= None
        self.node = node 
        print "node", node
        return node
    
    # destroy node on GCE
    def destroy(self, instances=None, destroydisks=True, force = False):
        node = self.updateNode()
        # detatch disks and destroy if not needed
        for disk in self.read_disks:
            if not force and node!=None: disk.detach(self)
            if destroydisks:
                disk.destroyifnotneeded(instances)
        for disk in self.read_write_disks:
            print disk.name, force, node, "about to detach"
            if not force and node!=None: disk.detach(self)
            if destroydisks: 
                disk.destroyifnotneeded(instances)
        # destroy node
        if node!=None and not self.destroyed:
            self.trycommand(self.gce_manager.destroy_node, node)
            node = None
            self.node=None
            self.printToLog("destroyed instance on GCE")
            # self.boot_disk.destroy() # boot disk seems to destroy itself so commenting this out
            self.destroyed=True
            self.created=False
        else:
            self.printToLog("mistakenly trying to destroy "+self.name+", destroyed "+str(self.destroyed)+" self.node "+str(self.node==None))
            self.destroyed=True
            self.created=False
    
    def packageShutdownScript(self, session):
        clientKey, clientSecret, tokenKey, tokenSecret = self._getClientAndAccessTokens(session)
        address = self.workflows[0].address
        return "\n".join(["#! /bin/bash",
                          "PID=$(pgrep -f Worker.py)",
                          # if Worker isn't running then the instance shutdown properly so exit
                          "if [[ \"$?\" -ne 0 ]]; then",
                          "echo \"Worker not running, shutting down immediately.\"",
                          "exit 0",
                          "fi",
                          # otherwise interupt the Worker.py program
                          "echo \"Sending SIGINT to $PID\"",
                          "kill -2 $PID",
                          "echo \"$PID is done\"",
                          # possibly write disk contents file but really not a good idea because there might be half complete files from the interupted command(s)
                          # "\n".join(map(lambda disk: disk.contentSave("/usr/local/bin/python2.7 "+self.rootdir+"DDCloudServer/DDServerApp/Utilities/writeDiskContentFile.py"), self.read_write_disks)),
                          # send preempted signal to server
                          "/usr/local/bin/python2.7 "+self.rootdir+"DDCloudServer/DDServerApp/Utilities/Worker.py --TK \""+tokenKey+"\" --TS \""+tokenSecret+"\" --CK "+clientKey+" --CS "+clientSecret + " --AD "+address + " --PR T"
                          ])
    
    # try command without erroring for some number of tries
    def trycommand(self, func, *args, **kwargs):
        tries = 0
        retries = 3
        while tries<retries:
            try:
                x = func(*args, **kwargs)
                return x
            except:
                e = sys.exc_info()[0]
                tries +=1
                time.sleep(10)
                self.printToLog(str(func) + " Error: "+str(e)+", "+str(e.__dict__)+ " try #"+str(tries)) 
        return None
                
    @staticmethod
    def findByName(session, name, user):
        from DDServerApp.ORM.Mappers.Workflow import Workflow, InstanceWorkflowLink
        iids=session.query(Instance).join(InstanceWorkflowLink).join(Workflow).filter(Instance.name==name).filter(Workflow.user_id==user.id).all()
        if len(iids)==0: return None
        else: return iids[0]  
        
    @staticmethod
    def findByID(session, iid):
        instances = session.query(Instance).filter(Instance.id==int(iid)).all()
        if len(instances)==0: return None
        else: return instances[0]

