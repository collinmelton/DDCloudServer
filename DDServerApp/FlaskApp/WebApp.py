'''
Created on Oct 20, 2014

@author: cmelton
'''

import sys, os, json, datetime, time
VERBOSE = True

path = os.getcwd().split("DDServerApp")[0]
if not path in sys.path:
    if VERBOSE: print path
    sys.path.insert(1, path)

from flask import Flask, url_for, render_template, session, request, redirect, flash, Markup, jsonify
from DDServerApp.ORM.Mappers import orm, User, UserUtilities
from DDServerApp.ORM import BASE_DIR
from DDServerApp.ORM.Mappers import Client, RequestToken, AccessToken, Nonce, Workflow, WorkflowTemplate, Image, DiskTemplate, InstanceTemplate, CommandTemplate, Credentials


# if '/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/' in os.getcwd(): #=='/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/ClinicalTrialStructuring/FlaskApp':
#     path = '/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/ClinicalTrialStructuring'
# else:
#     path = '/var/www/exact/ClinicalTrialStructuring'
#   
  
path = os.path.join(os.getcwd().split("DDServerApp")[0], "DDServerApp")
if not path in sys.path:
    if VERBOSE: print path
    sys.path.insert(1, path)
# del path


# import datetime

# import gviz_api, os, collections
from flask_bootstrap import Bootstrap
# from flask_wtf import Form
# from wtforms.validators import Required
# from wtforms import StringField, SubmitField
# from urllib2 import urlopen, build_opener
# import json

from flask_oauthlib.provider import OAuth1Provider



app = Flask(__name__)
app.config['PEMFILEFOLDER'] = os.path.join(BASE_DIR, "PemFiles")
Bootstrap(app)
oauth = OAuth1Provider(app)

app.secret_key='\x9f\x058.\x1a\xde\x7fn\xc6G\x08\xd0m|\xdd\xd0\xf6)\x80x8*+\xc5'
SESSION= orm.loadSession()
SESSION.rollback()
orm.Base.metadata.create_all()
app.config["JSON_SORT_KEY"] = False
app.config["OAUTH1_PROVIDER_REALMS"]=[""]
app.config["OAUTH1_PROVIDER_ENFORCE_SSL"] = False


app.config["LOGFILEDIRECTORY"] = os.path.join(BASE_DIR, "LogFiles")

def getTimeStampedFile(name):
    return name+"_"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')

def ensureDirectoryExists(mypath):
    if not os.path.exists(mypath): os.makedirs(mypath)
    return mypath


# app.config["OAUTH1_PROVIDER_SIGNATURE_METHODS"] = ( SIGNATURE_HMAC)


@app.route('/')
def index():
    '''
    This is the main page. It morphs into the users page when the user is logged in.
    '''
    user, redirect = getUser()
    if redirect!=None: return redirect
    return render_template('index_modern.html')

@app.route('/setup')
def setup():
    '''
    This is the main page. It morphs into the users page when the user is logged in.
    '''
    user, redirect = getUser()
    if redirect!=None: return redirect
    return render_template('setup_modern.html')

@app.route('/launcher')
def launcher():
    '''
    This is the main page. It morphs into the users page when the user is logged in.
    '''
    user, redirect = getUser()
    if redirect!=None: return redirect
    return render_template('launcher_modern.html')

@app.route('/dashboard')
def dashboard():
    '''
    This is the main page. It morphs into the users page when the user is logged in.
    '''
    user, redirect = getUser()
    if redirect!=None: return redirect
    return render_template('dashboard_modern.html')

# @app.route('/about', methods=['GET'])
# def about():
#     return render_template('about_modern.html')

@oauth.clientgetter
def load_client(client_key):
    '''
    This function loads the oauth client given a client key.
    A client getter is required. It tells which client is sending the requests.
    '''
    return Client.findFirst(client_key, SESSION)

@oauth.grantgetter
def load_request_token(token):
    '''
    This function loads a request token given the token.
    Request token & verifier getters and setters are required. They are used in the authorization flow.
    '''
    grant = RequestToken.findFirst(token, SESSION)
    return grant

@oauth.grantsetter
def save_request_token(token, request):
    '''
    This function saves the request token.
    Request token & verifier getters and setters are required. They are used in the authorization flow.
    '''
    if oauth.realms:
        realms = ' '.join(request.realms)
    else:
        realms = None
    grant = RequestToken(
        token=token['oauth_token'],
        secret=token['oauth_token_secret'],
        client=request.client,
        redirect_uri=request.redirect_uri,
        _realms=realms,
    )
    SESSION.add(grant)
    SESSION.commit()
    return grant

@oauth.verifiergetter
def load_verifier(verifier, token):
    '''
    Loads a verifier token.
    Request token & verifier getters and setters are required. They are used in the authorization flow.
    '''
    return RequestToken.findFirst(token, SESSION, verifier=verifier)

@oauth.verifiersetter
def save_verifier(token, verifier, *args, **kwargs):
    '''
    Adds a verifier token.
    Request token & verifier getters and setters are required. They are used in the authorization flow.
    '''
    tok = RequestToken.findFirst(token)
    tok.verifier = verifier['oauth_verifier']
    tok.user = getCurrentUser()
    SESSION.add(tok)
    SESSION.commit()
    return tok

def getCurrentUser():
    '''
    Gets the current user logged into the session.
    '''
    if 'username' not in session: return None
    return User.findUser(session['username'], SESSION)

@oauth.tokengetter
def load_access_token(client_key, token, *args, **kwargs):
    '''
    This function loads the access token given the client_key and token.
    '''
    t = AccessToken.findFirst(client_key, token, SESSION)
    return t

@oauth.tokensetter
def save_access_token(token, request):
    '''
    This function saves an access token.
    '''
    tok = AccessToken(
        client=request.client,
        user=request.user,
        token=token['oauth_token'],
        secret=token['oauth_token_secret'],
        _realms=token['oauth_authorized_realms'],
    )
    SESSION.add(tok)
    SESSION.commit()

@oauth.noncegetter
def load_nonce(client_key, timestamp, nonce, request_token, access_token):
    '''
    Finds the nonce.
    '''
    return Nonce.findFirst(client_key, timestamp, nonce, request_token, access_token, SESSION)

@oauth.noncesetter
def save_nonce(client_key, timestamp, nonce, request_token, access_token):
    '''
    Saves a nonce. The nonce ensures that a token is used one and in a certain time frame.
    '''
    nonce = Nonce(
        client_key=client_key,
        timestamp=timestamp,
        nonce=nonce,
        request_token=request_token,
        access_token=access_token,
    )
    SESSION.add(nonce)
    SESSION.commit()
    return nonce

# @app.route('/oauth/request_token')
# @oauth.request_token_handler
# def request_token():
#     '''
#     I believe the decorator takes care of returning something meaningful??
#     '''
#     return {}

# def require_login(func):
#     '''
#     At some point maybe should require that the user be logged in otherwise redirect.
#     For now don't worry about it because we want to skip the user authentication step.
#     '''
#     return func

# @app.route('/oauth/authorize', methods=['GET', 'POST'])
# @require_login
# @oauth.authorize_handler
# def authorize(*args, **kwargs):
#     '''
#     Returns the form if GET and if POST returns True if confirmation is yes.
#     Might not be useful for API calls but could always just POST directly to authorize.
#     For now if the client exists we will allow access and each worker instance will get a unique client id.
#     Actually we can call authorize as the instance is made and pass the request token as part of the startup script although
#     the nonce only last for 60 sec by default?
#     '''
# #     if request.method == 'GET':
#     return jsonify(request)
#     client_key = kwargs.get('resource_owner_key')
#     client = Client.findFirst(client_key, SESSION)
#     if client != None: return True
#     return False
#     kwargs['client'] = client
#         return render_template('authorize.html', **kwargs)
#     confirm = request.form.get('confirm', 'no')
#     return confirm == 'yes'

def parseVariables(d, varname="varname", varvalue = "varvalue"):
    varnames = [v for v in d.keys() if varname in v]
    varvalues = [v for v in d.keys() if varvalue in v]
    pairids = [n.split("_")[1] for n in varnames]
    result = {}
    for id in pairids:
        name = ""
        value = ""
        for v in varnames: 
            if v.split("_")[1] == id: name = v
        for v in varvalues: 
            if v.split("_")[1] == id: value = v
        result[d[name]]=d[value]
    return result

def getID(name):
    if ":" not in str(name):
        return None
    return name.split(":")[0]



def newWorkflow(user, data, new, delete):
    if delete:
        wfid = getID(request.form["workflowWorkflowsSelect"])
        WorkflowTemplate.delete(SESSION, wfid, user)
        result = {"updates": {}, "message": "deleted workflow"}
    elif new:
        credID = getID(data["workflowCredentialsSelect"])
        if credID == None: credentials = None
        else: credentials = Credentials.findByID(SESSION, credID, user)
        nwf = WorkflowTemplate(data["newWorkflowName"], user, credentials=credentials)
        SESSION.add(nwf)
        SESSION.commit()
        result = {"updates":{"workflows":{str(nwf.id):nwf.dictForJSON()}},
                  "message": "added new workflow"}
    else:
        wfid = getID(request.form["workflowVarWorkflowsSelect"])
        wf = WorkflowTemplate.findByID(SESSION, wfid, user)
        if VERBOSE: print user.name, user.id
        if wf == None: return {"updates": {}, "message": "user permissions error"}        
        newvars = parseVariables(request.form)
        wf.updateVarDict(newvars, user)
        result = {"updates":{"workflows":{str(wf.id):wf.dictForJSON()}},
                  "message": "updated workflow"}
    return result

def saveImage(user, data, delete):
    imageID = getID(data["imageImagesSelect"])
    name = data["imageNameOnImageForm"]
    if imageID == "0": return {"updates": {}, "message": "deleted image"}
    authAccount = data["authAccount"]
    rootdir = data["installDirectory"]
    if imageID == None:
        image = Image(name, authAccount, rootdir, user)
        SESSION.add(image)
        SESSION.commit()
    elif delete:
        Image.delete(SESSION, imageID, user)
        return {"updates": {}, "message": "deleted image"}
    else:
        image = Image.findByID(SESSION, imageID, user)
        if image != None:
            image.updateValues(name, authAccount, rootdir, user)
            SESSION.add(image)
            SESSION.commit()
        else:
            return {"updates": {}, "message": "user permissions error on image"}
#             image = Image(name, authAccount, user) 
    result = {"updates":{"images":{str(image.id):image.dictForJSON()}},
              "message": "updated image"}
    return result

def saveDisk(user, data, variables, delete):
    if delete:
        diskID = getID(data["diskDisksSelect"])
        workflow = WorkflowTemplate.findByID(SESSION, getID(data["diskWorkflowsSelect"]), user)
        if workflow == None: return {"updates": {}, "message": "user permissions error on workflow"}
        if diskID!=None:
            DiskTemplate.delete(SESSION, diskID, user)
    elif variables:
        diskID = getID(data["diskVarDisksSelect"])
        workflow = WorkflowTemplate.findByID(SESSION, getID(data["diskVarWorkflowsSelect"]), user)
        if workflow == None: return {"updates": {}, "message": "user permissions error on workflow"}   
        disk = DiskTemplate.findByID(SESSION, diskID, user)
        if disk==None: return {"updates": {}, "message": "user permissions error on disk"}
        disk.updateVarDict(parseVariables(data), user)
    else:
        diskID = getID(data["diskDisksSelect"])
        workflow = WorkflowTemplate.findByID(SESSION, getID(data["diskWorkflowsSelect"]), user)
        if workflow == None: return {"updates": {}, "message": "user permissions error on workflow"}
        name = data["diskName"]
        if getID(data["diskImagesSelect"])=="0": 
            image = None
        else: 
            image = Image.findByID(SESSION, getID(data["diskImagesSelect"]), user)
            if image == None: return {"updates": {}, "message": "user permissions error on image"}
        diskSize = data["diskSize"]
        diskType = data["diskTypeSelector"]
        location = data["diskLocationSelector"]
        if VERBOSE: print "diskID", diskID
        if diskID == None:
            disk = DiskTemplate(name.lower(), workflow, image, diskSize, diskType, location)
        else:
            disk = DiskTemplate.findByID(SESSION, diskID, user)
            if disk != None:
                disk.updateValues(name.lower(), workflow, image, diskSize, diskType, location, user)
            else:
                return {"updates": {}, "message": "user permissions error on disk"}
#                 disk = DiskTemplate(name, workflow, image, diskSize, diskType, location)
    SESSION.add(workflow)
    SESSION.commit()
    result = {"updates":{"workflows":{str(workflow.id):workflow.dictForJSON()}},
              "message": "updated disk"}
    return result

def allowedFile(filename):
    return len(filename)>4 and filename[-4:]==".pem"

def saveCredentials(user, data, files, delete):
    name = data["credentialsName"]
    serviceAccount = data["serviceAccountEmail"]
    project = data["project"]
    f = request.files['pemFileUpload']
    
    credID = getID(data["credentialCredentialsSelect"])
    # get credentials object
    if credID == None:
        cred = Credentials("", "", "", "",user)
    else:
        cred = Credentials.findByID(SESSION, credID, user)
        if cred == None: return {"updates": {}, "message": "user permissions error on credentials"}
    # process inputs
    if f and allowedFile(f.filename):
        filename = str(user.id)+".pem"
        f.save(os.path.join(app.config['PEMFILEFOLDER'], filename))
        pemFileLocation = os.path.join(app.config['PEMFILEFOLDER'], filename)
    else:
        pemFileLocation = ""
    # update values
    if delete:
        Credentials.delete(SESSION, cred.id, user)
    else:
        cred.updateValues(name.lower(), serviceAccount, pemFileLocation, project)
        SESSION.add(cred)
        SESSION.commit()
    return {"updates": {"credentials": {c.id: c.dictForJSON() for c in user.credentials}},
            "message": "updated credentials"}

def saveCommand(user, data, delete):
    workflow = WorkflowTemplate.findByID(SESSION, getID(data["workflowInCommandForm"]), user)
    if workflow == None: return {"updates": {}, "message": "user permissions error on workflow"}
    if delete:
        cid = getID(data["commandInCommandForm"])
        if cid!=None:
            CommandTemplate.delete(SESSION, cid, user)    
    else:
        instance = InstanceTemplate.findByID(SESSION, getID(data["instanceInCommandForm"]), user)
        if instance == None: return {"updates": {}, "message": "user permissions error on instance"}
        name = data["CommandName"]
        commandText = data["Command"]
        commandID = getID(data["commandInCommandForm"])
        dependencies = [CommandTemplate.findByID(SESSION, cid, user) for cid in list(set([getID(idname) for idname in data.getlist("commandDependenciesSelect")]))]
        if None in dependencies: return {"updates": {}, "message": "user permissions error on command dependencies"}
        ## edit old command or make new command
        if commandID != None:
            command = CommandTemplate.findByID(SESSION, commandID, user)
            if command == None: 
                return {"updates": {}, "message": "user permissions error on command"}
            command.updateValues(instance, name.lower(), commandText, dependencies)
        else:
            command = CommandTemplate(instance, name.lower(), commandText, dependencies)
            SESSION.add(command)
            SESSION.commit()

    result = {"updates":{"workflows":{str(workflow.id):workflow.dictForJSON()}},
              "message": "updated command"}
    SESSION.add(workflow)
    SESSION.commit()
    return result
        

def saveInstance(user, data, variables, delete):
    if delete:
        if VERBOSE: print "deleting"
        workflow = WorkflowTemplate.findByID(SESSION, getID(data["instanceWorkflowsSelect"]), user)
        if workflow == None: return {"updates": {}, "message": "user permissions error on workflow"}
        iid = getID(data["instanceInstancesSelect"])
        if iid!=None:
            if VERBOSE: print iid
            InstanceTemplate.delete(SESSION, iid, user)
        workflow = WorkflowTemplate.findByID(SESSION, getID(data["instanceWorkflowsSelect"]), user)
    elif variables:
        workflow = WorkflowTemplate.findByID(SESSION, getID(data["instanceVarWorkflowsSelect"]), user)
        if workflow == None: return {"updates": {}, "message": "user permissions error"}
        if VERBOSE: print "got workflow"
        instID = getID(data["instanceVarInstancesSelect"])
        if instID == None: return {"updates": {}, "message": "instance id error"}
        instance = InstanceTemplate.findByID(SESSION, instID, user)
        if VERBOSE: print "got instance"
        if instance == None: return {"updates": {}, "message": "user permissions error"}
        instance.updateVarDict(parseVariables(data), user)
        if VERBOSE: print "updated vars"
    else:
        workflow = WorkflowTemplate.findByID(SESSION, getID(data["instanceWorkflowsSelect"]), user)
        if workflow == None: return {"updates": {}, "message": "user permissions error on workflow"}
        name = data["instanceName"]
        machineType = data["instanceMachineTypeSelector"]
        location = data["instanceLocationSelector"]
        bootDisk = DiskTemplate.findByID(SESSION, getID(data["instanceBootDiskSelect"]), user)
        if bootDisk==None: return {"updates": {}, "message": "user permissions error on boot disk"}
        readDisks = [DiskTemplate.findByID(SESSION, did, user) for did in list(set([getID(idname) for idname in data.getlist("instanceReadDisksSelect")]))]
        if None in readDisks: return {"updates": {}, "message": "user permissions error on read disks"}
        readWriteDisks = [DiskTemplate.findByID(SESSION, did, user) for did in list(set([getID(idname) for idname in data.getlist("instanceReadWriteDisksSelect")]))]
        if None in readWriteDisks: return {"updates": {}, "message": "user permissions error on read/write disks"}
        instID = getID(data["instanceInstancesSelect"])
        dependencies = [InstanceTemplate.findByID(SESSION, iid, user) for iid in list(set([getID(idname) for idname in data.getlist("instanceDependenciesSelect")]))]
        if None in dependencies: return {"updates": {}, "message": "user permissions error on instance dependencies"}
        if VERBOSE: print "test"
        ex_tags = data["ex_tags"]
        if VERBOSE: print ex_tags
        ex_metadata = data["ex_metadata"]
        if VERBOSE: print ex_metadata
        ex_network = data["ex_network"]
        if VERBOSE: print ex_network
        numLocalSSD = data["numLocalSSD"]
        if VERBOSE: print numLocalSSD
        if "preemptible" not in data:
            preemptible = False
        else:
            preemptible = (data["preemptible"]=="T")
        if VERBOSE: print preemptible
        ## edit old instance or make new instance
        if instID != None:
            if VERBOSE: print "updating instance"
            instance = InstanceTemplate.findByID(SESSION, instID, user)
            if instance == None: 
#                 instance = InstanceTemplate(name, machineType, location, bootDisk, readDisks, 
#                                         readWriteDisks, dependencies, workflow)
                return {"updates": {}, "message": "user permissions error on instance"}
            instance.updateValues(name.lower(), machineType, location, bootDisk, readDisks, 
                                  readWriteDisks, dependencies, ex_tags, ex_metadata,
                                  ex_network, numLocalSSD, preemptible)
        else:
            if VERBOSE: print "adding instance"
            instance = InstanceTemplate(name.lower(), machineType, location, bootDisk, readDisks, 
                                        readWriteDisks, dependencies, workflow, ex_tags, 
                                        ex_metadata, ex_network, numLocalSSD, preemptible)
    SESSION.add(workflow)
    SESSION.commit()
    result = {"updates":{"workflows":{str(workflow.id):workflow.dictForJSON()}},
              "message": "updated instance"}
    return result  

@app.route("/api/_getuserdata", methods=['GET'])
def getUserData():
    user = getCurrentUser()
    if VERBOSE: print user.getUserData()
    return jsonify({"data": user.getUserData(),
            "message": "updated data"})

@app.route("/api/_getdashboarddata", methods=['GET'])
def getDashboardData():
    user = getCurrentUser()
    requestType = request.args["type"]
    if requestType == "instances":
        data = user.getWorkflowInstancesData(request.args["workflow_id"])
#         data = {"colnames":[["string", "key1", "Key1"],
#                         ["string", "key2", "Key2"]],
#             "rows":  [{"key1": {"value":"<a onclick='toggleCommands(\"1\");'>Instance 1</a>", "css":""},
#                        "key2": {"value":"1-2", "css":""}},
#                       {"key1": {"value":"<a onclick='toggleCommands(\"2\");'>Instance 2</a>", "css":""},
#                        "key2": {"value":"2-2", "css":""}}
#                         ],
#             "numrows":2}
    elif requestType == "commands":
        data = user.getInstanceCommandData(request.args["workflow_id"], request.args["instance_id"])
#         data = {"colnames":[["string", "key1", "Name"],
#                         ["string", "key2", "Result"]],
#             "rows":  [{"key1": {"value":"<a onclick='toggleCommand(\"1\");'>Command 1</a>", "css":""},
#                        "key2": {"value":"result 1", "css":""}},
#                       {"key1": {"value":"<a onclick='toggleCommand(\"2\");'>Command 2</a>", "css":""},
#                        "key2": {"value":"result 2", "css":""}}
#                         ],
#             "numrows":2}
    elif requestType == "performance":
        data = user.getPerformanceData(request.args["workflow_id"], request.args["instance_id"], request.args["command_id"])
#         data = [['Time', 'CPU', 'Memory', 'Write', 'Read'],
#         ['1',  100,      1, 10, 1],
#         ['2',  15,      34, 10, 1],
#         ['3',  50,       55, 10, 1],
#         ['4',  5,      40, 10, 1]]
    elif requestType == "workflows":
        data = user.getWorkflowsDashboardData()
#         data = {"1":{"id":"1", "name": "test1", "names":["1_name1", "1_name2"]}, 
#                 "2":{"id":"2", "name": "test1", "names":["2_name1", "2_name2"]}}
    else: data = ""
    print data
    return jsonify({"data": data,
            "message": "hello!"})

def workflowLauncher(user, data, stop):
    if stop:
        wfid = getID(request.form["activeWorkflowSelect"])
    else:
        wfid = getID(request.form["launcherWorkflowSelect"])
    if VERBOSE: print "finding workflow"
    wf = WorkflowTemplate.findByID(SESSION, wfid, user)
    if VERBOSE: print "found workflow"
    if wf == None: return {"updates": {}, "message": "user permissions error for workflow"}
    if not stop:
        if VERBOSE: print os.path.join(app.config["LOGFILEDIRECTORY"], user.name)
        if VERBOSE: print getTimeStampedFile(wf.name)
        if VERBOSE: print os.path.join(ensureDirectoryExists(os.path.join(app.config["LOGFILEDIRECTORY"], user.name)), getTimeStampedFile(wf.name))
        logfilename = os.path.join(ensureDirectoryExists(os.path.join(app.config["LOGFILEDIRECTORY"], user.name)), getTimeStampedFile(wf.name))
        if VERBOSE: print logfilename
        address = request.url_root
        if VERBOSE: print address
        wf.startWorkflow(SESSION, logfilename, address)
    else:
        if VERBOSE: print "stopping workflow"
        wf.stopWorkflow(SESSION)
    return {"updates": {"active_workflows": user.getActiveWorkflows()},  
            "message": "started workflow"}

# def workflowLauncher(user, data, stop):
#     wft = WorkflowTemplate.findByID(SESSION, getID(data["launcherWorkflowSelect"]), user)
#     if wft == None: return {"updates": {}, "message": "user permissions error on workflow template"}
#     if wft.workflows == []:
#         logfilename = os.path.join(ensureDirectoryExists(os.path.join(app.config["LOGFILEDIRECTORY"], user.name)), getTimeStampedFile(wft.name)) 
#         wf = Workflow(wft.name, wft, user, logfilename)
#     else:
#         wf = wft.workflows[0]
#     if wf.active: 
#         return {"updates": {}, "message": "workflow is already active"}
#     else: 
#         wf.start()
#         return {"updates": {}, "message": "workflow has been started!"}
    
    
@app.route("/api/_workflows", methods=['POST'])
def workflowEditor():
    if VERBOSE: print request.form
    if VERBOSE: print request.form.getlist
    user = getCurrentUser()
    updatetype = request.form["submitType"]
    edittype = request.form["editType"]
    result = {"message":"test message", "updates":"test updates"}
    formData = request.form
    if VERBOSE: print updatetype
    if updatetype=="workflow":
        result = newWorkflow(user, formData, edittype=="new", edittype=="delete")
    elif updatetype=="disk":
        result = saveDisk(user, formData, edittype=="variables", edittype=="delete")
    elif updatetype=="image":
        result = saveImage(user, formData, edittype=="delete")
    elif updatetype=="instance":
        result = saveInstance(user, formData, edittype=="variables", edittype=="delete")
    elif updatetype=="command":
        result = saveCommand(user, formData, edittype=="delete")
    elif updatetype=="credentials":
        result = saveCredentials(user, formData, request.files, edittype=="delete")
    elif updatetype=="launchworkflow":
        result = workflowLauncher(user, formData, edittype=="stop")
    if VERBOSE: print result
    return jsonify(result)

@app.route('/oauth/access_token')
@oauth.access_token_handler
def access_token():
    return {}

@app.route('/api/me')
@oauth.require_oauth('full')
def me():
    '''
    Returns user info in json form.
    '''
    return jsonify({"this":"worked!"})
    user = request.oauth.user
    return jsonify(username=user.name)

@app.route('/api/commands', methods=['GET', 'POST'])
@oauth.require_oauth('full')
def commands():
    '''
    Returns command info in json form.
    '''
    if request.method == "GET":
        client = request.oauth.client
        return jsonify({c.id: c.toSummary() for c in client.instance.commands})
    else:
        client = request.oauth.client
        if VERBOSE: print "command update:", request.data
        client.instance.updateCommandData(json.loads(request.data), SESSION)
        SESSION.add(client.instance)
        SESSION.commit()        
        return jsonify({"this":"worked!"})


@app.route('/api/finish', methods=['GET'])
@oauth.require_oauth('full')
def finish():
    '''
    Returns command info in json form.
    '''
    if VERBOSE: print "FINISHING!!!"
    if request.method == "GET":
        client = request.oauth.client
        if VERBOSE: print "finishing"
        return jsonify(client.instance.finish(SESSION))

# @app.route('/trial/', methods=['GET','POST'])
# def annotatenewtrial():
#     user, trialannotationset, redirect_return = getUserAndTrial(None, redirect_dest="index")
#     if redirect_return != None: return redirect_return
#     if trialannotationset == None:
#         trialannotationset=ClinicalTrial.getUnannotatedTrial(user, SESSION, WORDSETS)
#     return redirect(url_for('show_trial_data', tid=trialannotationset.id))


# @app.route('/_updatedata', methods=['GET'])
# def getTrialPageElementsData():
#     tid = request.args.get('tid', 0, type=int)
#     type = request.args.get('type', "none", type=str)
#     print tid, type
#     user, redirect_return = getUser(redirect_dest="index")
#     if redirect_return != None: return jsonify({"message":"redirect error", "updates": {}})
#     result = {}
#     if type == "drug":
#         content = "\n".join(map(lambda name: "<option value=\""+name+"\">"+name+"</option>", [d.name for d in trialannotationset.drugs+trialannotationset.potentialnewdrugs]))
#         result = {"message": "", "updates": [{"type":"select", "name":'drugtoremove', "value":content}]}
#     if type == "cancer":
#         content = "\n".join(map(lambda name: "<option value=\""+name+"\">"+name+"</option>", [c.name for c in [ca.cancer for ca in trialannotationset.cancerannos]+trialannotationset.potentialnewcancers]))
#         result = {"message": "", "updates": [{"type":"select", "name":'cancertoremove', "value":content}]}
#     if type == "alteration":
#         content = "\n".join(map(lambda name: "<option value=\""+name+"\">"+name+"</option>", [str(a.id)+": "+str(a) for a in trialannotationset.clinicaltrialalterations]))
#         result = {"message": "", "updates": [{"type":"select", "name":'alterationtoremove', "value":content}]}
#     if type == "status":
#         content = "Annotation Finalized:&nbsp" + str(trialannotationset.annotated)
#         result = {"message": "", "updates": [{"type":"h2", "name":"trial_annotation_status", "value":content}]}
#     return jsonify(result)    

# def expanderWrapHTML(text, id, splittype=" ", length=1, addontosnippet=""):
#     if len(text)<30: return text
#     if "</a>" in text: return text # dont wrap in expander if its a link
#     if "</form>" in text: return text
#     if len(text.split(splittype))<1: 
#         snippet = text
#     else:
#         snippet = splittype.join(text.split(splittype)[0:min(len(text.split(splittype)), length)])
#         if snippet == text: return text
#         snippet+=addontosnippet
#     if snippet != text: snippet+=" ..."
#     expander = "<div onClick=\"openClose('"+str(id)+"')\" id=\"closer_"+str(id)+"\" class=\"texter_closer\" style=\"text-align: center; display:block;\">"+snippet+"<br /><br />\n</div>\n"
#     expander += "<div onClick=\"openClose('"+str(id)+"')\" id=\"expander_"+str(id)+"\" class=\"texter\" style=\"text-align: center;  display:none;\">"+text+"<br /><br />\n</div>"
#     return expander
# 
# def getTableJSONData(description, rows, length=1):
#     result = {}
#     result["numrows"]=len(rows)
#     rowdicts = [dict([(key, {"value":expanderWrapHTML(val, str(id)+"_"+key.replace(" ", "_"), splittype=" ", length=length), "css":'text-align:center;'}) for key, val in row.items()]) for id, row in rows]
#     result["rows"]=rowdicts
#     result["colnames"]=[(val[0], val[1], key) for key, val in description.items()]
#     return result
# 
# def getTrialDrugTableData(trialannotationset):
#     toshow = trialannotationset.drugs+trialannotationset.potentialnewdrugs
#     if len(toshow)==0: return {}
#     description = toshow[0].getGvisTableData(trialannotationset.id)["description"]
#     rows = map(lambda drug: ("dr"+str(drug.id), drug.getGvisTableData(trialannotationset.id)["data"]), toshow)    
#     return getTableJSONData(description, rows)
# 
def getUser(redirect_dest="index"):
    user, redirect_return = None, None
    if 'username' not in session:
        flash("You requested a restricted access page. Please login.")
        if VERBOSE: print "You requested a restricted access page. Please login."
        redirect(url_for('login'))
        redirect_return = redirect(url_for('login'))
    else:
        user = User.findUser(session["username"], SESSION)
    return user, redirect_return

@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    message = ""
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']
        password_confirmation = request.form['passwordconfirmation']
        role = request.form['role']
        if password!=password_confirmation:
            message = "error: password and password confirmation don't match"
        else:
            user = User.newUser(username, role, password, SESSION)
            if user == None:
                message = "error: username already in use"
            else:
                session['username'] = user.name
                if "admin" in user.role: 
                    session["admin"]=True
                else: 
                    session["admin"]=False
            return redirect(url_for('index'))
    return render_template('newuser_modern.html', error=message)
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    This page allows user to login to see his/her patients or to upload new patient data.
    '''
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']
        user = User.login(username, password, SESSION)
        error = None
        if isinstance(user, basestring):
            error = user
            if VERBOSE: print error
        else:
            session['username'] = user.name
            if "admin" in user.role: 
                session["admin"]=True
            else: 
                session["admin"]=False
            if VERBOSE: print 'You were successfully logged in'
            return redirect(url_for('index'))
        if VERBOSE: print session["username"]
        return render_template('login_modern.html', error=error)
    return render_template('login_modern.html')

@app.route('/logout')
def logout():
    '''
    This page allows the user to logout.
    '''
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
#     
# if app.debug is not True:   
#     import logging
#     from logging.handlers import RotatingFileHandler
#     file_handler = RotatingFileHandler('python.log', maxBytes=1024 * 1024 * 100, backupCount=20)
#     file_handler.setLevel(logging.ERROR)
#     formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#     file_handler.setFormatter(formatter)
#     app.logger.addHandler(file_handler)

# app.run(debug=True)
if __name__ == '__main__':
#     import logging
#     from logging.handlers import RotatingFileHandler
#     file_handler = RotatingFileHandler('python.log', maxBytes=1024 * 1024 * 100, backupCount=20)
#     file_handler.setLevel(logging.ERROR)
#     formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#     file_handler.setFormatter(formatter)
#     app.logger.addHandler(file_handler)
    import logging
    logging.basicConfig()
    app.run(debug=True) # debug must be off on production for security reasons