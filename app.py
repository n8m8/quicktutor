from flask import Flask, render_template, request, redirect, session, jsonify
from pythonsql import *
import json
from dbRequests import *
app = Flask(__name__)

##### Front End Routes #####

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/test")
def test():
	return "test123"

@app.route("/kian")
def kian():
	return render_template('dashboard.html')


##### Web Service Routes #####

### DEMO WEB SERVICE ROUTE ###

@app.route('/request/submitTestForm', methods=['POST'])
def request_submitTestForm():
	firstname = request.form['firstname']
	lastname = request.form['lastname']
	print("Name:", firstname, lastname)
	return redirect('/kian')

### Authentication ###
# createAccount
@app.route("/auth/createaccount", methods=['POST'])
def auth_createAccount():
	email = request.form['email']
	displayname = request.form['displayname']
	password = request.form['password']
	return "notImplementedException"

# login
@app.route("/auth/login", methods=['POST'])
def auth_login():
	email = request.form['email']
	password = request.form['password']
	return "notImplementedException"

@app.route('/login', methods=['POST'])
def login():
	user_name = checkUsername(request.form['username'])
	pwd = checkPassword(request.form['password'])
	if user_name != -1:
		session['user_name'] = user_name
		session['pwd'] = pwd
		session['logged_in'] = True
	elif request.form['username'] == 'admin':
		session['admin'] = True
		session['logged_in'] = True
	return redirect('/')

@app.route('/logout')
def logout():
	session['user_name'] = -1
	session['admin'] = False
	session['logged_in'] = False
	return redirect('/')

@app.route('/request/getUserInfo', methods=['GET'])
def request_getUserInfo():
	if request.method == 'GET':
		sampleJsonData = '[{"userid": 1, "email": "test@case.edu", "password": "password", "displayname": "TestUser"}]'
		return sampleJsonData
# forgotPassword
@app.route("/auth/forgotpassword/", methods=['POST'])
def auth_forgotpassword():
	email = request.form['email']
	return "notImplementedException"


### Main Activity Page / Listings ###
# getlistings
@app.route("/listings/getall", methods=['GET'])
def listings_getall():
	return "notImplementedException"

# createlistings
@app.route("/listings/create", methods=['POST'])
def listings_create():
	email = request.form['email']
	location = request.form['location']
	cclass = request.form['cclass']
	description = request.form['description']
	return "notImplementedException"

# createlistings
@app.route("/request/respond", methods=['POST'])
def listings_respond():
	email = request.form['email']
	listingId = request.form['listingId']
	return "notImplementedException"


### Messages ###
# sendmessage
@app.route("/msg/send", methods=['POST'])
def msg_send():
	originId = request.form['originId']
	destId = request.form['destId']
	return "notImplementedException"

# receivemessages
@app.route("/msg/receive", methods=['POST'])
def msg_receive():
	return "notImplementedException"


### Profile ###
# get a profile
@app.route("/profile/get", methods=['GET'])
def profile_get():
	return "notImplementedException"

# ChangeScreenName
@app.route("/profile/changescreenname", methods=['POST'])
def profile_changescreenname():
	newName = request.form['newName']
	return "notImplementedException"

# AddClass
@app.route("/profile/addclass", methods=['POST'])
def profile_addclass():
	classDept = request.form['classDept']
	classNum = request.form['classNum']
	return "notImplementedException"

# RemoveClass
@app.route("/profile/removeclass/<classDept>/<classNum>", methods=['POST'])
def profile_removeclass():
	classDept = request.form['classDept']
	classNum = request.form['classNum']
	return "notImplementedException"

if __name__ == "__main__":
	app.run()

# http://flask.pocoo.org/docs/0.12/quickstart/ #
