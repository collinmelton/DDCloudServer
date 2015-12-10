'''
Created on Dec 5, 2015

@author: cmelton
'''
import unittest, json
from Worker import Communicator, Worker

from DDServerApp.ORM.Mappers import orm, User, InstanceCommand, Client, Instance
from DDServerApp.Utilities.JobAndDiskFileReader import JobAndDiskFileReader
from DDServerApp.Utilities.LogFile import LogFile
from DDServerApp.Utilities.GCEManager import GCEManager

SESSION= orm.loadSession()
# orm.Base.metadata.drop_all()
orm.Base.metadata.create_all()

class Test(unittest.TestCase):




    def getCommunicator(self):
        # oauth 1 credentials
        token_key = 'wmMc3ETYGcg9a6MCkXcl5LZGs'
        token_secret = 'w2H2B37P1zOdrD0ryeF3jpGVw'
        client_props = {'client_secret': u'MQWsHSVWyCIqZhIeZ0doOetHI', 'client_key': u'x1LofvxeO1PVaxivWFF78aCU7'}
        client_key = client_props['client_key']
        client_secret = client_props['client_secret']
        # communicate with oauth1
        return Communicator(client_key, client_secret, token_key, token_secret)

    def testOauth1Server(self):
        c = self.getCommunicator()
        result = c.get("http://127.0.0.1:5000/api/me")
        self.assertTrue("this" in result._content and "worked!" in result._content, "server call and oauth1 is working")

    def testFetchCommands(self):
        c = self.getCommunicator()
        result = json.loads(c.get("http://127.0.0.1:5000/api/commands")._content)
        self.assertTrue(all([key in result[result.keys()[0]].keys() for key in ["command", "command_dependencies", "command_type", "id"]]))
    
    def getWorker(self):
        token_key = 'wmMc3ETYGcg9a6MCkXcl5LZGs'
        token_secret = 'w2H2B37P1zOdrD0ryeF3jpGVw'
        client_props = {'client_secret': u'MQWsHSVWyCIqZhIeZ0doOetHI', 'client_key': u'x1LofvxeO1PVaxivWFF78aCU7'}
        client_key = client_props['client_key']
        client_secret = client_props['client_secret']
        return Worker(token_key, token_secret, client_key, client_secret, "test instance")
    
    def getCommands(self):
        worker = self.getWorker()
        return worker.getCommands()
    
    def testWorkerFetchCommands(self):
        # add commands only if db has been reset
        #self.addCommandsOnServer()
        commands = self.getCommands()
        self.assertTrue("InstanceCommand" in str(type(commands[0])), "fetch commands error")

    def testGetFirstCommands(self):
        commands = self.getCommands()
        firstcommands = InstanceCommand.getFirstCommands(commands)
        # do first commands have any dependencies in all commands
        allIDs = [c.id for c in commands]
        self.assertTrue(all([all([cd.id not in allIDs for cd in c.command_dependencies]) for c in firstcommands]), "first commands have dependencies in all commands")
        
    def testRunCommands(self):
        worker = self.getWorker()
        worker.run()
        for c in worker.commands:
            print c.finished, c.failed, c.result
        
        
        
#         self.assertTrue("InstanceCommand" in str(type(firstcommands[0])), "fetch commands error")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()