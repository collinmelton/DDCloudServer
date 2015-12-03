'''
Created on Oct 20, 2014

@author: cmelton
'''

import sys, os

path = os.getcwd().split("DDServerApp")[0]
if not path in sys.path:
    print path
    sys.path.insert(1, path)

from flask import Flask, url_for, render_template, session, request, redirect, flash, Markup, jsonify
from DDServerApp.ORM.Mappers import orm, User, UserUtilities
from DDServerApp.ORM import BASE_DIR

# if '/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/' in os.getcwd(): #=='/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/ClinicalTrialStructuring/FlaskApp':
#     path = '/Users/cmelton/Documents/AptanaStudio3WorkspaceNew/ClinicalTrialStructuring'
# else:
#     path = '/var/www/exact/ClinicalTrialStructuring'
#     
path = os.path.join(os.getcwd().split("DDServerApp")[0], "DDServerApp")
if not path in sys.path:
    print path
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

app = Flask(__name__)
Bootstrap(app)

app.secret_key='\x9f\x058.\x1a\xde\x7fn\xc6G\x08\xd0m|\xdd\xd0\xf6)\x80x8*+\xc5'
SESSION= orm.loadSession()
SESSION.rollback()
app.config["JSON_SORT_KEY"] = False


@app.route('/')
def index():
    '''
    This is the main page. It morphs into the users page when the user is logged in.
    '''
    if 'username' in session:
        user = User.findUser(session["username"], SESSION)
    return render_template('index_modern.html')

# @app.route('/trial/', methods=['GET','POST'])
# def annotatenewtrial():
#     user, trialannotationset, redirect_return = getUserAndTrial(None, redirect_dest="index")
#     if redirect_return != None: return redirect_return
#     if trialannotationset == None:
#         trialannotationset=ClinicalTrial.getUnannotatedTrial(user, SESSION, WORDSETS)
#     return redirect(url_for('show_trial_data', tid=trialannotationset.id))


@app.route('/about', methods=['GET'])
def about():
    return render_template('about_modern.html')


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
# def getUser(redirect_dest="index"):
#     user, redirect_return = None, None, None, None
#     if 'username' not in session:
#         flash("You requested a restricted access page. Please login.")
#         print "You requested a restricted access page. Please login."
#         redirect(url_for('login'))
#         redirect_return = redirect(url_for('login'))
#     else:
#         user = User.findUser(session["username"], SESSION)
#     return user, redirect_return

# @app.route('/newuser', methods=['GET', 'POST'])
# def newuser():
#     message = ""
#     if request.method == 'POST':
#         username = request.form['login']
#         password = request.form['password']
#         password_confirmation = request.form['passwordconfirmation']
#         role = request.form['role']
#         if password!=password_confirmation:
#             message = "error: password and password confirmation don't match"
#         else:
#             user = User.newUser(username, role, password, SESSION)
#             if user == None:
#                 message = "error: username already in use"
#             else:
#                 session['username'] = user.name
#                 if "admin" in user.role: 
#                     session["admin"]=True
#                 else: 
#                     session["admin"]=False
#             return redirect(url_for('index'))
#     return render_template('newuser_modern.html', error=message)
# 
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     '''
#     This page allows user to login to see his/her patients or to upload new patient data.
#     '''
#     if "WEBAUTH_USER" in request.environ:
#         username = request.environ["WEBAUTH_USER"]
#         print username
#         user = User.findUser(username, SESSION) 
#         
#         if user == None: 
#             user = User(username, "doctor", "password")
#             orm.Base.metadata.create_all()
#             PatientAndUserUtilities.addAllToDB(SESSION)
#         session['username'] = username
#         if "admin" in user.role: 
#             session["admin"]=True
#         else: 
#             session["admin"]=False
#         return redirect(url_for('index'))
#          
#     if request.method == 'POST':
#         username = request.form['login']
#         password = request.form['password']
#         user = User.login(username, password, SESSION)
#         error = None
#         if isinstance(user, basestring):
#             error = user
#             flash(error)
#         else:
#             session['username'] = user.name
#             if "admin" in user.role: 
#                 session["admin"]=True
#             else: 
#                 session["admin"]=False
#             flash('You were successfully logged in')
#             return redirect(url_for('index'))
#         return render_template('login_modern.html', error=error)
#     return render_template('login_modern.html')
# 
# @app.route('/logout')
# def logout():
#     '''
#     This page allows the user to logout.
#     '''
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('index'))
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
    app.run(debug=True) # debug must be off on production for security reasons