'''
Created on Nov 30, 2015

@author: cmelton
'''
import unittest
from DDServerApp.ORM.Mappers import orm, User, InstanceCommand
from DDServerApp.Utilities.JobAndDiskFileReader import JobAndDiskFileReader
from DDServerApp.Utilities.LogFile import LogFile
from DDServerApp.Utilities.GCEManager import GCEManager

SESSION= orm.loadSession()
orm.Base.metadata.drop_all()
orm.Base.metadata.create_all()

class Test(unittest.TestCase):

    def testAddingInstancesAndDisks(self):
        auser = User.findUser("Jane", SESSION)
        if auser ==None:
            auser = User("Jane", "user", "password")
        log = LogFile("/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/DDCloudServer/Data/TestFiles/testLog.txt")
        myDriver = GCEManager("875996339847-nv3l8p9pp4ervtpsg1gbpbabktd619db@developer.gserviceaccount.com", 
                              "/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/DDCloudServer/Data/TestFiles/GCP_SnyderProject.pem",
                              "875996339847-compute@developer.gserviceaccount.com", 
                              project="gbsc-gcp-lab-snyder")
        job_csv_file = "/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/DDCloudServer/Data/TestFiles/test_instances_lssd-pre-0010.csv" 
        disk_csv_file = "/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/DDCloudServer/Data/TestFiles/test_disks_lssd-pre-0010.csv"
        jadf=JobAndDiskFileReader(job_csv_file, disk_csv_file, myDriver, log, "/home/cmelton/", StackdriverAPIKey="", activateStackDriver=False)
        instances, disks = jadf.readInJobInfo(session=SESSION)
        auser.addDisks(disks.values())
        auser.addInstances(instances.values())
        SESSION.add_all(instances.values())
        SESSION.add_all(disks.values())
        SESSION.add_all([auser])
        SESSION.commit()
        
    def testViewingInstances(self):
        auser = User.findUser("Jane", SESSION)
        if auser ==None:
            auser = User("Jane", "user", "password")
        instances = auser.instances
        print [i.name for i in instances]
        
    def testCommandSorting(self):
        auser = User.findUser("Jane", SESSION)
        if auser ==None:
            auser = User("Jane", "user", "password")
        instance = auser.instances[-1]
        log = LogFile("/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/DDCloudServer/Data/TestFiles/testLog.txt")
        myDriver = GCEManager("875996339847-nv3l8p9pp4ervtpsg1gbpbabktd619db@developer.gserviceaccount.com", 
                              "/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/DDCloudServer/Data/TestFiles/GCP_SnyderProject.pem",
                              "875996339847-compute@developer.gserviceaccount.com", 
                              project="gbsc-gcp-lab-snyder")
        instance.reinit(myDriver, log)
        sortedDict = InstanceCommand.getOrderedCommandsByInstance(instance)
        originalDict = instance.parseScript()
        print [c.command for c in originalDict["main"]]
        print [c.command for c in sortedDict["main"]]
        self.assertEquals([c.command for c in originalDict["main"]], [c.command for c in sortedDict["main"]], "test command sorting doesn't work")
#         self.assertEquals(originalDict["main"], sortedDict["main"], "test command sorting doesn't work")
#         self.assertEquals(originalDict["shutdown"], sortedDict["shutdown"], "test command sorting doesn't work")

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()