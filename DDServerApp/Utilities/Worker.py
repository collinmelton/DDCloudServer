'''
Created on Dec 3, 2015

@author: cmelton
'''

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
        
    def post(self, url, body, headers = None):
        '''
        Takes in body and header and returns response in json format.
        '''
        if VERBOSE: print "body:", body
        if headers == None:
            response = self.client.post(url, auth=self.oauth,data=json.dumps(body, cls = MyJSONEncoder))
        else:
            response = self.client.post(url, auth=self.oauth,data=json.dumps(body, cls = MyJSONEncoder), headers=headers)
        return json.loads(response.content)
    
    def get(self, url):
        '''
        Takes in body and header and returns response in json format.
        '''
        response = self.client.get(url, auth=self.oauth)
        return response
        return json.loads(response.content)

class Worker(object):
    '''
    This class runs all the code on a worker instance. 
    This class's run method is invoked in the startup script on each worker instance. 
    '''

    def __init__(self, token_key, token_secret, client_key, client_secret, instance_name):
        self.token_key = token_key
        self.token_secret = token_secret
        self.client_key = client_key
        self.client_secret = client_secret
        self.instance_name = instance_name
        self.first_commands = []
        self.communicator = self._initCommunicator()
#         self.getCommands()
    
    def _initCommunicator(self):
        '''
        This method initializes the communicator.  The communicator is the object 
        that uses Oauth1 to communicate with the master instance. 
        '''
        return Communicator(self.client_key, self.client_secret, self.token_key, self.token_secret)
    
    def _sendData(self, data, data_type):
        '''
        This method sends data to the master instance.
        '''
        pass
    
    def _getData(self, data_type):
        '''
        This method sends data to the master instance.
        '''
        pass
    
    def updateCommandData(self, data):
        result = self.communicator.post("http://127.0.0.1:5000/api/commands", data)
        if VERBOSE: print result
        
    
    def getCommands(self):
        '''
        This method communicates with the master node and gets all commands to run.
        '''
        commandString = self.communicator.get("http://127.0.0.1:5000/api/commands")._content
        self.commands = InstanceCommand.generateCommandsFromJSON(commandString)
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
        
    
    
        
    

if __name__ == "__main__":
    
    token_key = 'TWuEjpsLpabBe6ImkdG37PbtX'
    token_secret = '7GslLWSHTa0jblFCl9hk33oiJ'
    client_props = {'client_secret': u's8rPirVz7uLF0vNmwHCKMCzxL', 'client_key': u'hdqLvlmpcWOsnHPQHGyRG9V5O'}
    client_key = client_props['client_key']
    client_secret = client_props['client_secret']

    c = Communicator(client_key, client_secret, token_key, token_secret)
#     if VERBOSE: print c.get("http://127.0.0.1:5000/api/me")
    result = c.get("http://127.0.0.1:5000/api/me")
    if VERBOSE: print result._content
    if VERBOSE: print result.request.__dict__
    body = {'title':'Test dataset', 'description':'Test description','defined_type':'dataset'}
    headers = {'content-type':'application/json'}
        
        
        