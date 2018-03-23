from flask import Flask, render_template, request, redirect, session, jsonify
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

@app.route("/dashboard")
def kian():
	return render_template('dashboard.html')


##### Web Service Routes #####

### DEMO WEB SERVICE ROUTE ###

@app.route('/request/submitTestForm', methods=['POST'])
def request_submitTestForm():
	print(request.form)
	return redirect('/dashboard')

### Authentication ###
# signup
@app.route("/auth/signup", methods=['POST'])
def auth_signup():
	email = request.form['signupemail']
	# displayname = request.form['displayname']
	password = request.form['signuppassword']
	addUser((email, password, 'fillerusername',))
	return redirect('/')

# Login
@app.route('/auth/login', methods=['POST'])
def login():
	# print(request.form)
	userId = validateUserData((request.form['loginemail'], request.form['loginpassword'],))
	print(userId)
	if userId != -1:
		session['user_name'] = userId
		session['pwd'] = request.form['loginpassword']
		session['logged_in'] = True
		if request.form['loginemail'].lower() == 'qtadmin@case.edu':
			session['admin'] = True
	else:
		session['user_name'] = -1
		session['admin'] = False
		session['logged_in'] = False
		print(session)
		return "Login information was not valid."

	return redirect('/dashboard')

@app.route('/auth/logout', methods=['POST'])
def logout():
	session.pop('user_name', None)
	return redirect('/')

@app.route('/request/getBasicInfo', methods=['GET'])
def request_getBasicInfo():
	if request.method == 'GET':
		print(session)
		if 'user_name' in session:
			return getUsernameFromUserId((session['user_name'],))
		else:
			return "User did not exist"

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
	listings = dbRequests.getAllListings()
	return listings

# createlistings
@app.route("/listings/create", methods=['POST'])
def listings_create():
	email = request.form['email']
	location = request.form['location']
	classID = request.form['classID']
	description = request.form['description']
	dbRequests.addListing(())
	return "notImplementedException"

# createlistings
@app.route("/request/respond", methods=['POST'])
def listings_respond():
	email = request.form['email']
	listingId = request.form['listingId']
	addHelpPair(email, listingId)
	return "notImplementedException"


### Messages ###
# sendmessage
@app.route("/msg/send", methods=['POST'])
def msg_send():
	originId = request.form['originId']
	destId = request.form['destId']
	messagecontents = request.form['messagecontents']
	addMessage(originId, destId, messagecontents)
	return "notImplementedException"

# receivemessages
@app.route("/msg/receive", methods=['POST'])
def msg_receive():
	userId = request.form['userId']
	messages = dbRequests.getAllMessages(userId)
	return messages


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
	dbRequests.addRuserClass(session['user_name'], classDept, classNum)
	return "notImplementedException"

# RemoveClass
@app.route("/profile/removeclass", methods=['POST'])
def profile_removeclass():
	userId = request.form['userId']
	classDept = request.form['classDept']
	classNum = request.form['classNum']
	dbRequests.deleteRuserClass(userId, classDept, classNum)
	return "notImplementedException"

if __name__ == "__main__":
	app.secret_key = "3sAmVAtdh!GNTSKuZJJn4^5wve"
	app.run()

# http://flask.pocoo.org/docs/0.12/quickstart/ #
