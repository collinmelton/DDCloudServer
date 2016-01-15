'''
Created on Dec 3, 2015

@author: cmelton
'''


import sys, os, inspect, thread, time

path = inspect.getfile(inspect.currentframe()).split("DDServerApp")[0]
print path
if not path in sys.path:
    print path
    sys.path.insert(1, path)

import requests
from requests_oauthlib import OAuth1
import json
import datetime
from time import mktime
from DDServerApp.ORM.Mappers import InstanceCommand, RunCommandThread

VERBOSE = False

class MyJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return float(mktime(obj.timetuple())+float(obj.microsecond)/1000000)

        return json.JSONEncoder.default(self, obj)

class Communicator(object):
    '''
    For now this class just recieves communications from the WebApp.
    '''

    def __init__(self, client_key, client_secret, token_key,
                 token_secret):
        '''
        Constructor
        '''
        # get oauth object
        self.oauth = OAuth1(client_key=client_key, client_secret=client_secret,
               resource_owner_key=token_key, resource_owner_secret=token_secret,
               signature_type = 'auth_header')
        # get request session
        self.client = requests.session()
        self.sleeptime=10
        self.retries = 5
        
    def post(self, url, body, headers = None):
        '''
        Takes in body and header and returns response in json format.
        '''
        counter = 0
        while counter<self.retries:
            if VERBOSE: print "body:", body
            if headers == None:
                response = self.client.post(url, auth=self.oauth,data=json.dumps(body, cls = MyJSONEncoder))
            else:
                response = self.client.post(url, auth=self.oauth,data=json.dumps(body, cls = MyJSONEncoder), headers=headers)
            try: return json.loads(response._content)
            except: counter+=1
            time.sleep(self.sleeptime)
        return {}
        
    
    def get(self, url, retries=None):
        '''
        Takes in body and header and returns response in json format.
        '''
        if retries == None: retries = self.retries
        counter = 0
        while counter<retries:
            response = self.client.get(url, auth=self.oauth)
            try: return json.loads(response._content)
            except: counter+=1
            time.sleep(self.sleeptime)
        return {}

class Worker(object):
    '''
    This class runs all the code on a worker instance. 
    This class's run method is invoked in the startup script on each worker instance. 
    '''

    def __init__(self, token_key, token_secret, client_key, client_secret, base_address):
        self.token_key = token_key
        self.token_secret = token_secret
        self.client_key = client_key
        self.client_secret = client_secret
        self.first_commands = []
        self.communicator = self._initCommunicator()
        self.base_address = base_address
        self.lock=thread.allocate_lock()
#         self.getCommands()
    
    def _initCommunicator(self):
        '''
        This method initializes the communicator.  The communicator is the object 
        that uses Oauth1 to communicate with the master instance. 
        '''
        return Communicator(self.client_key, self.client_secret, self.token_key, self.token_secret)
    
    def updateCommandData(self, data):
        self.lock.acquire()
        print "posting data"
        result = self.communicator.post(self.base_address.strip("/")+"/api/commands", data)
        self.lock.release()
        if VERBOSE: print result
        
    
    def getCommands(self):
        '''
        This method communicates with the master node and gets all commands to run.
        '''
        print self.base_address+"/api/commands"
        commandData = self.communicator.get(self.base_address.strip("/")+"/api/commands")
        print "commands from server:", commandData
        self.commands = InstanceCommand.generateCommandsFromDataDict(commandData)
        return self.commands 
    
    def run(self):
        # first get commands
        self.getCommands()
        if VERBOSE: print self.commands
        for c in self.commands: c.finished = False
        # next get first commands
        self.first_commands = InstanceCommand.getFirstCommands(self.commands)
        # add commands to run to a queue
        threads = []
        for command in self.first_commands:
            threads.append(RunCommandThread(command, worker = self))
        # start all threads, when each thread finishes command it starts a new set of 
        # threads for yet to be completed and ready commands and waits for them to
        # complete, so when the initial threads are finished all threads are finished
        for thread in threads:
            thread.start()
        # what for threads to finish
        for thread in threads:
            thread.join()
            
    def finish(self):
        self.communicator.get(self.base_address.strip("/")+"/api/finish")
        
    def preempted(self):
        self.communicator.get(self.base_address.strip("/")+"/api/preempted", retries=1)
        
from optparse import OptionParser

# this functions gets the command line options for running the program
def getOptions():
    parser = OptionParser()
    parser.add_option("--TK", dest = "tokenKey", help = "", metavar = "STRING", type = "string")
    parser.add_option("--TS", dest = "tokenSecret", help = "", metavar = "STRING", type = "string")
    parser.add_option("--CK", dest = "clientKey", help = "", metavar = "STRING", type = "string")
    parser.add_option("--CS", dest = "clientSecret", help = "", metavar = "STRING", type = "string")
    parser.add_option("--AD", dest = "address", help = "", metavar = "STRING", type = "string")
    parser.add_option("--PR", dest = "preempted", help = "", metavar = "STRING", type = "string", default = "F")
    (options, args) = parser.parse_args()
    return options    
    
if __name__ == "__main__":

    options = getOptions()
    w = Worker(options.tokenKey, options.tokenSecret, options.clientKey, options.clientSecret, options.address)
    
    if options.preempted == "T":
        print "preempting"
        w.preempted()
    else:
        w.run()
        w.finish()
#     token_key = 'TWuEjpsLpabBe6ImkdG37PbtX'
#     token_secret = '7GslLWSHTa0jblFCl9hk33oiJ'
#     client_props = {'client_secret': u's8rPirVz7uLF0vNmwHCKMCzxL', 'client_key': u'hdqLvlmpcWOsnHPQHGyRG9V5O'}
#     client_key = client_props['client_key']
#     client_secret = client_props['client_secret']
# 
#     c = Communicator(client_key, client_secret, token_key, token_secret)
# #     if VERBOSE: print c.get("http://127.0.0.1:5000/api/me")
#     result = c.get("http://127.0.0.1:5000/api/me")
#     if VERBOSE: print result._content
#     if VERBOSE: print result.request.__dict__
#     body = {'title':'Test dataset', 'description':'Test description','defined_type':'dataset'}
#     headers = {'content-type':'application/json'}
        
        
        