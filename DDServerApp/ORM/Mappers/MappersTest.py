'''
Created on Nov 30, 2015

@author: cmelton
'''
import unittest
from DDServerApp.ORM.Mappers import orm, User, InstanceCommand, Client, Instance, AccessToken, WorkflowTemplate, Image, DiskTemplate, InstanceTemplate, CommandTemplate, Workflow, Disk
from DDServerApp.Utilities.JobAndDiskFileReader import JobAndDiskFileReader
from DDServerApp.Utilities.LogFile import LogFile
from DDServerApp.Utilities.GCEManager import GCEManager

SESSION= orm.loadSession()
# orm.Base.metadata.drop_all()
orm.Base.metadata.create_all()

class Test(unittest.TestCase):

#     def testAddingInstancesAndDisks(self):
#         auser = User.findUser("Jane", SESSION)
#         if auser ==None:
#             auser = User("Jane", "user", "password")
#         log = LogFile("/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/DDCloudServer/Data/TestFiles/testLog.txt")
#         myDriver = GCEManager("875996339847-nv3l8p9pp4ervtpsg1gbpbabktd619db@developer.gserviceaccount.com", 
#                               "/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/DDCloudServer/Data/TestFiles/GCP_SnyderProject.pem",
#                               "875996339847-compute@developer.gserviceaccount.com", 
#                               project="gbsc-gcp-lab-snyder")
#         job_csv_file = "/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/DDCloudServer/Data/TestFiles/test_instances_lssd-pre-0010.csv" 
#         disk_csv_file = "/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/DDCloudServer/Data/TestFiles/test_disks_lssd-pre-0010.csv"
#         jadf=JobAndDiskFileReader(job_csv_file, disk_csv_file, myDriver, log, "/home/cmelton/", StackdriverAPIKey="", activateStackDriver=False)
#         instances, disks = jadf.readInJobInfo(session=SESSION)
#         auser.addDisks(disks.values())
#         auser.addInstances(instances.values())
#         SESSION.add_all(instances.values())
#         SESSION.add_all(disks.values())
#         SESSION.add_all([auser])
#         SESSION.commit()

    def getUser(self):
        user = User.findUser("Jane", SESSION)
        if user ==None:
            user = User("Jane", "user", "password")
        return user
    
    def getWorkflowTemplate(self, vardict = {}):
        user = self.getUser()
        wft = WorkflowTemplate.findByName(SESSION, "test_workflow_template", user)
        if wft==None:
            wft = WorkflowTemplate("test_workflow_template", user, workflowVars={"$1":"collin"})
        wft.updateVarDict(vardict, user)
        return wft
    
    def getImage(self):
        user = self.getUser()
        image = Image.findByName(SESSION, "test_image", user)
        if image==None:
            image = Image("test_image", "875996339847-compute@developer.gserviceaccount.com", "/home/cmelton/", user)
        return image
    
    def testWorkflowTemplate(self):
        wft = self.getWorkflowTemplate()
        self.assertTrue(wft != None, "error generating workflow template")
    
    def testImage(self):
        image = self.getImage()
        self.assertTrue(image != None, "error generating image")
        
    def getBootDiskTemplate(self, workflow=None, vardict = {}):
        if workflow==None: workflow = self.getWorkflowTemplate()
        image = self.getImage()
        user = self.getUser()
        disk = DiskTemplate.findByName(SESSION, "test_boot_disk_template", user)
        if disk == None:
            disk = DiskTemplate("test_boot_disk_template", workflow, image, 10, "pd-standard", "us-central1-a")
        disk.updateVarDict(vardict, disk.workflow.user)
        return disk
    
    def getReadDiskTemplates(self, workflow=None, vardict = {}):
        if workflow==None:
            workflow = self.getWorkflowTemplate()
        image = self.getImage()
        user = self.getUser()
        disk = DiskTemplate.findByName(SESSION, "test_read_disk_template", user)
        if disk == None:
            disk = DiskTemplate("test_read_disk_template", workflow, image, 100, "pd-standard", "us-central1-a")
        disk.updateVarDict(vardict, disk.workflow.user)
        return [disk]
    
    def getReadWriteDiskTemplates(self, workflow=None, vardict = {}):
        if workflow==None: workflow = self.getWorkflowTemplate()
        image = self.getImage()
        user = self.getUser()
        disk = DiskTemplate.findByName(SESSION, "test_read_write_disk_template", user)
        if disk == None:
            disk = DiskTemplate("test_read_write_disk_template", workflow, image, 100, "pd-standard", "us-central1-a")
        disk.updateVarDict(vardict, disk.workflow.user)
        return [disk]
    
    def testDiskTemplate(self):
        disk = self.getBootDiskTemplate()
        self.assertTrue(disk!=None, "error generating disk template")
        
    def getInstanceTemplate(self, workflow=None, vardict = {}):
        if workflow==None: 
            workflow = self.getWorkflowTemplate()
            user = workflow.user
        else:
            user = self.getUser()
        it = InstanceTemplate.findByName(SESSION, "test_instance_template", user)
        if it==None:
            it = InstanceTemplate("test_instance_template", "f1-micro", "us-central1-a", self.getBootDiskTemplate(workflow=workflow, vardict=vardict),
                                  self.getReadDiskTemplates(workflow=workflow, vardict=vardict), self.getReadWriteDiskTemplates(workflow=workflow, vardict=vardict), 
                                  [], workflow, "tag1|tag2", "key1:value1|key2:value2", "", 1, True)
        it.updateVarDict(vardict, it.workflow.user)
        return it
    
    def testInstanceTemplate(self):
        it = self.getInstanceTemplate()
        self.assertTrue(it!=None, "error generating instance template")
        
    def getCommandTemplate(self, command_name, dependencies=[], instance=None):
        if instance==None: instance = self.getInstanceTemplate()
        user = self.getUser()
        ct = CommandTemplate.findByName(SESSION, command_name, user)
        if ct==None:
            ct = CommandTemplate(instance, command_name, "echo hello", dependencies)
        return ct
    
    def testCommandTemplate(self):
        ct1 = self.getCommandTemplate("test_command_1", [])
        self.assertTrue(ct1 != None, "error generating command template")
    
    def getWorkflow(self, wft=None):
        if wft==None: wft = self.getWorkflowTemplate()
        user = self.getUser()
        wf = Workflow.findByName(SESSION, "test_workflow", user)
        if wf == None:
            wf = Workflow("test_workflow", wft, user)
        return wf
    
    def testWorkflow(self):
        wf = self.getWorkflow()
        self.assertTrue(wf != None, "error generating workflow")
    
    def getDisk(self, disk_name):
        user = self.getUser()
        disk = Disk.findByName(SESSION, disk_name, user)
        if disk==None:
            disk = Disk(disk_name, 10, "us-central1-a", snapshot=None, image=None, disk_type='pd-standard', 
                        init_source="", shutdown_dest="")
        return disk
    
    def getBootDisk(self):
        return self.getDisk("test_boot_disk") 
    
    def getReadDisk(self):
        return self.getDisk("test_read_disk")
    
    def getReadWriteDisk(self):
        return self.getDisk("test_read_write_disk")
    
    def testDisk(self):
        disk = self.getBootDisk()
        self.assertTrue(disk!=None, "error creating disk")
    
    def getInstance(self):
        user = self.getUser()
        inst = Instance.findByName(SESSION, 'test_instance', user)
        dependency_names=[]
        command_dict = {'1': {'dependencies': [], 'command': u"echo 'hello'\r\nsleep 10", 'id': '1', 'name': u'Command 1'}, '2': {'dependencies': ['1'], 'command': u"echo 'hello 2'", 'id': '2', 'name': u'Command 2'}}
        inst = Instance.findByName(SESSION, 'test_instance', user)
        if inst == None:
            inst = Instance('test_instance', "f1-micro", self.getImage(), "us-central1-a", "", 
                            "tag1|tag2", "key1:value1|key2:value2", dependency_names, 
                            [self.getReadDisk()], [self.getReadWriteDisk()], self.getBootDisk(), 
                            command_dict, rootdir="/home/cmelton/", preemptible=True, numLocalSSD=0, 
                            localSSDInitSources="", localSSDDests="")
        return inst
    
    def testInstance(self):
        inst = self.getInstance()
        self.assertTrue(inst!=None, "error generating instance")
    
    def getCommand(self):
        user = self.getUser()
        instance = self.getInstance()
        command = "echo 'test!'"
        c = InstanceCommand.findByCommand(SESSION, command, user)
        if c == None:
            c = InstanceCommand(instance, command, [], "main")
        return c
    
    def testCommand(self):
        command = self.getCommand()
        self.assertTrue(command!=None, "error generating command")
    
    def testWorkflowToDisksAndInstances(self):
        workflowtemplate = self.getWorkflowTemplate()
        instanceTemplate = self.getInstanceTemplate(workflow=workflowtemplate)
        commandTemplate = self.getCommandTemplate("test command", [], instanceTemplate)
        workflow = self.getWorkflow(wft=workflowtemplate)
        disks = workflow.createDisksInNamedDict()
        self.assertTrue(type(disks.values()[0])==Disk, "error generating disks from workflow")
        instances = workflow.createInstancesInNamedDict(disks)
        self.assertTrue(type(instances.values()[0])==Instance, "error generating instances from workflow")
        self.assertTrue(type(instances.values()[0].commands[0])==InstanceCommand, "error generating commands from instance")
    
    def initWorkflow(self, workflowvardict={}, diskinstancevardict = {}):
        workflowtemplate = self.getWorkflowTemplate(vardict = workflowvardict)
        instanceTemplate = self.getInstanceTemplate(workflow=workflowtemplate, vardict = diskinstancevardict)
        commandTemplate = self.getCommandTemplate("test command", [], instanceTemplate)
        workflow = self.getWorkflow(wft=workflowtemplate)
        workflow.initDisksAndInstances()
        return workflow
    
    def testWorkflowInit(self):
        workflow = self.initWorkflow()
        self.assertTrue(type(workflow.disks[0])==Disk, "error generating disks from workflow")
        self.assertTrue(type(workflow.instances[0])==Instance, "error generating instances from workflow") 
    
    def testWorkflowVars(self):
        workflow = self.initWorkflow(workflowvardict={"test":"test1,test2"}, diskinstancevardict = {"template":"template1,template2"})
        # test workflow var replacement
        diskNames = {"test1":[d.name.replace("test1", "test") for d in workflow.disks if "test1" in d.name], 
                     "test2":[d.name.replace("test2", "test") for d in workflow.disks if "test2" in d.name]}
        instanceNames = {"test1":[i.name.replace("test1", "test") for i in workflow.instances if "test1" in i.name], 
                     "test2":[i.name.replace("test2", "test") for i in workflow.instances if "test2" in i.name]}
        commands = {"test1":reduce(lambda x,y: x+y, [[d.command.replace("test1", "test") for d in i.commands] for i in workflow.instances if "test1" in i.name]), 
                     "test2":reduce(lambda x,y: x+y, [[d.command.replace("test2", "test") for d in i.commands] for i in workflow.instances if "test2" in i.name])}
        self.assertEquals(list(set(diskNames["test1"]) - set(diskNames["test2"])), [], "workflowvar replacement failed")
        self.assertEquals(list(set(instanceNames["test1"]) - set(instanceNames["test2"])), [], "workflowvar replacement failed")
        self.assertEquals(list(set(commands["test1"]) - set(commands["test2"])), [], "workflowvar replacement failed")
        
        # test disk and instance var replacement
        diskNames = {"test1":[d.name.replace("template1", "template") for d in workflow.disks if "template1" in d.name], 
                     "test2":[d.name.replace("template2", "template") for d in workflow.disks if "template2" in d.name]}
        instanceNames = {"test1":[i.name.replace("template1", "template") for i in workflow.instances if "template1" in i.name], 
                     "test2":[i.name.replace("template2", "template") for i in workflow.instances if "template2" in i.name]}
        self.assertEquals(list(set(diskNames["test1"]) - set(diskNames["test2"])), [], "workflowvar replacement failed")
        self.assertEquals(list(set(instanceNames["test1"]) - set(instanceNames["test2"])), [], "workflowvar replacement failed")

#     def makeTestInstanceWithSimpleCommands(self):
#         auser = self.getUser()
#         log = LogFile("/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/DDCloudServer/Data/TestFiles/testLog.txt")
#         myDriver = GCEManager("875996339847-nv3l8p9pp4ervtpsg1gbpbabktd619db@developer.gserviceaccount.com", 
#                               "/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/DDCloudServer/Data/TestFiles/GCP_SnyderProject.pem",
#                               "875996339847-compute@developer.gserviceaccount.com", 
#                               project="gbsc-gcp-lab-snyder")
#         
#         # create instance
#         instance1 = Instance("test", "", "", [], [], None, myDriver, "echo hello\nsleep 10\necho goodbye", log, session=SESSION)
#         instance1.commands = []
#         # create simple commands
#         command1 = InstanceCommand(instance1, "echo hello1\nsleep 15", [], "main")
#         command2 = InstanceCommand(instance1, "echo hello2\nsleep 15", [command1], "main")
#         return instance1
# #         SESSION.add_all([instance1])
# #         SESSION.commit()
# 
#     def testClient(self):
#         auser = User.findUser("Jane", SESSION)
#         if auser ==None:
#             auser = User("Jane", "user", "password")
#         client_props = {'client_secret': u'MQWsHSVWyCIqZhIeZ0doOetHI', 'client_key': u'x1LofvxeO1PVaxivWFF78aCU7'}
#         c = Client.findFirst(client_props["client_key"], SESSION)
#         if c==None:
#             instance = self.makeTestInstanceWithSimpleCommands()
#             # need to add
#             print "couldn't find client"
#             c = Client("test", "a test client", auser, ["full"], [], instance)
#             SESSION.add_all([c])
#             SESSION.commit()
#             ac = c.createAccessToken(SESSION)
#         ac = AccessToken.findFirst(c.client_key, None, SESSION)
#         SESSION.add_all([ac])
#         SESSION.commit()
#         print ac
#         print c.getClientCredentials()
        
#     def testViewingInstances(self):
#         auser = User.findUser("Jane", SESSION)
#         if auser ==None:
#             auser = User("Jane", "user", "password")
#         instances = auser.instances
#         print [i.name for i in instances]
#         
#     def testCommandSorting(self):
#         auser = User.findUser("Jane", SESSION)
#         if auser ==None:
#             auser = User("Jane", "user", "password")
#         instance = auser.instances[-1]
#         log = LogFile("/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/DDCloudServer/Data/TestFiles/testLog.txt")
#         myDriver = GCEManager("875996339847-nv3l8p9pp4ervtpsg1gbpbabktd619db@developer.gserviceaccount.com", 
#                               "/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/DDCloudServer/Data/TestFiles/GCP_SnyderProject.pem",
#                               "875996339847-compute@developer.gserviceaccount.com", 
#                               project="gbsc-gcp-lab-snyder")
#         instance.reinit(myDriver, log)
#         sortedDict = InstanceCommand.getOrderedCommandsByInstance(instance)
#         originalDict = instance.parseScript()
#         print [c.command for c in originalDict["main"]]
#         print [c.command for c in sortedDict["main"]]
#         self.assertEquals([c.command for c in originalDict["main"]], [c.command for c in sortedDict["main"]], "test command sorting doesn't work")
#         self.assertEquals(originalDict["main"], sortedDict["main"], "test command sorting doesn't work")
#         self.assertEquals(originalDict["shutdown"], sortedDict["shutdown"], "test command sorting doesn't work")

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()