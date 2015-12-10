'''
Created on Nov 30, 2015

@author: cmelton
'''
import unittest
from DDServerApp.ORM.Mappers import orm, User, InstanceCommand, Client, Instance, AccessToken
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

    def makeTestInstanceWithSimpleCommands(self):
        auser = User.findUser("Jane", SESSION)
        if auser ==None:
            auser = User("Jane", "user", "password")
        log = LogFile("/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/DDCloudServer/Data/TestFiles/testLog.txt")
        myDriver = GCEManager("875996339847-nv3l8p9pp4ervtpsg1gbpbabktd619db@developer.gserviceaccount.com", 
                              "/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/DDCloudServer/Data/TestFiles/GCP_SnyderProject.pem",
                              "875996339847-compute@developer.gserviceaccount.com", 
                              project="gbsc-gcp-lab-snyder")
        
        # create instance
        instance1 = Instance("test", "", "", [], [], None, myDriver, "echo hello\nsleep 10\necho goodbye", log, session=SESSION)
        instance1.commands = []
        # create simple commands
        command1 = InstanceCommand(instance1, "echo hello1\nsleep 15", [], "main")
        command2 = InstanceCommand(instance1, "echo hello2\nsleep 15", [command1], "main")
        return instance1
#         SESSION.add_all([instance1])
#         SESSION.commit()

    def testClient(self):
        auser = User.findUser("Jane", SESSION)
        if auser ==None:
            auser = User("Jane", "user", "password")
        client_props = {'client_secret': u'MQWsHSVWyCIqZhIeZ0doOetHI', 'client_key': u'x1LofvxeO1PVaxivWFF78aCU7'}
        c = Client.findFirst(client_props["client_key"], SESSION)
        if c==None:
            instance = self.makeTestInstanceWithSimpleCommands()
            # need to add
            print "couldn't find client"
            c = Client("test", "a test client", auser, ["full"], [], instance)
            SESSION.add_all([c])
            SESSION.commit()
            ac = c.createAccessToken(SESSION)
        ac = AccessToken.findFirst(c.client_key, None, SESSION)
        SESSION.add_all([ac])
        SESSION.commit()
        print ac
        print c.getClientCredentials()
        
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