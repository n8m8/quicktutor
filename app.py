from flask import Flask, render_template, request, redirect, session, jsonify
from flask_mail import Mail
from flask_socketio import SocketIO, join_room, leave_room
from werkzeug.security import generate_password_hash, check_password_hash
import json, re, string, random
from activation import *
from dbRequests import *
import config

app = Flask(__name__)
app.config.from_object('config')
mail = Mail(app)

##### Front End Routes #####

@app.route("/")
def index():
	if session['logged_in'] == True:
		return redirect('/dashboard')
	else:
		return render_template('index.html')

@app.route("/test")
def test():
	return "test123"

@app.route("/dashboard")
def dashboard():
	print(session)
	if session['logged_in'] == True:
		return render_template('dashboard.html')
	else:
		return redirect('/')


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

	# Validate email
	regex = re.compile('(^[a-zA-Z0-9_.+-]+@(?:(?:[a-zA-Z0-9-]+\.)?[a-zA-Z]+\.)?(case)\.edu$)')
	regexResult = regex.match(email)

	# Validate Password
	pwregex = re.compile('(?=^.{8,}$)(?=.*\d)(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$')
	pwResult = pwregex.search(password)

	if regexResult != None:
		existingUserId = lookupUserIdFromEmail((email,))

		if existingUserId == -1:
			if pwResult != None:
				addUser((email, generate_password_hash(password), email,))
				activationToken = make_email_token(email)
				sendActivationEmail(email, activationToken)
				return 'Almost done! Check your email to activate your account.'
			else:
				return "Password did not meet strength requirements."
		else:
			return "That email is already taken!"
	else:
		return "Invalid email address. Please use a valid @case.edu address."

# activate
@app.route("/auth/activate/<token>", methods=['GET'])
def auth_activate(token):
	plaintextEmail = confirm_email_token(token)
	if plaintextEmail == False:
		return "Invalid email activation token."
	else:
		didConfirm = confirmUser((plaintextEmail,))
		if didConfirm == True:
			return "Account successfully activated! Go log in."
		else:
			return "Unable to confirm user. Maybe your account is already activated, or your activation token expired."


# forgotPassword
@app.route("/auth/forgotpassword", methods=['POST'])
def auth_forgotpassword():
	email = request.form['email']

	userid = getUserIdFromEmail((email,))
	if userid is None:
		return "There is no account associated with that email address!"
	else:
		newpassword = ""
		while len(newpassword) < 8:
			newpassword = newpassword + random.choice(string.ascii_letters + string.digits)
			changeUserPassword((generate_password_hash(newpassword), email,))

		return "Your password was reset! Check your email for your new password."


# Login
@app.route('/auth/login', methods=['POST'])
def login():
	# print(request.form)
	# userId = validateUserData((request.form['loginemail'], request.form['loginpassword'],))
	hashedPassword = getHashedPassword((request.form['loginemail'],))

	if hashedPassword is None:
		return "There is no account associated with that email address."

	matches = check_password_hash(hashedPassword, request.form['loginpassword'])

	if matches:
		session['user_name'] = request.form['loginemail']
		session['pwd'] = hashedPassword
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
	session['logged_in'] = False
	session['admin'] = False
	return redirect('/')

@app.route('/request/getUserInfo', methods=['GET'])
def request_getUserInfo():
	if request.method == 'GET':
		sampleJsonData = '[{"userid": 1, "email": "test@case.edu", "password": "password", "displayname": "TestUser"}]'
		return sampleJsonData

### Main Activity Page / Listings ###
# getlistings
@app.route("/listings/getall", methods=['GET'])
def listings_getall():
	listings = getAllListings()

	ret = []

	for item in listings:
		new = {}
		new['listingid'] = item[0]
		new['userid'] = item[1]
		new['classid'] = item[2]
		new['shortDescription'] = item[3]
		new['topic'] = item[4]
		new['timestamp'] = item[5]
		ret.append(new)

	return json.dumps(ret)

# createlistings
@app.route("/listings/create", methods=['POST'])
def listings_create():
	email = request.form['email']
	location = request.form['location']
	classID = request.form['classID']
	description = request.form['description']
	try:
		userid = getUserIdFromEmail((email,))
		dbRequests.addListing((userid, classID, description, location,))
		return 'success'
	except:
		return "database error"

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
	if request.method == 'GET':
		if 'user_name' in session:
			ret = {}
			ret['email'] = session['user_name']
			ret['screenname'] = getUsernameFromUserEmail((session['user_name'],))
			userClassIds = getClassesForUser((session['user_name'],))
			if userClassIds is None:
				ret['classes'] = []
			else:
				ret['classes'] = []
				for classid in userClassIds:
					newclass = {}
					newclass['classid'] = classid[0]
					newclass['stringName'] = getClassStringName(classid)
					ret['classes'].append(newclass)
			return json.dumps(ret)
		else:
			return "User did not exist"
	else:
		return "Invalid protocol for this route, use GET"

# ChangeScreenName
@app.route("/profile/changescreenname", methods=['POST'])
def profile_changescreenname():
	newName = request.form['newName']
	changeUserScreenname((newName, session['user_name']))
	return "Changed screennname!"

# AddClass
@app.route("/profile/addclass", methods=['POST'])
def profile_addclass():

	classDept = request.form['classDept']
	classNum = request.form['classNum']
	addRuserClass((session['user_name'], classDept, classNum,))
	return "Added your class!"

# RemoveClass
@app.route("/profile/removeclass", methods=['POST'])
def profile_removeclass():
	classDept = request.form['classDept']
	classNum = request.form['classNum']
	deleteRuserClass((session['user_name'], classDept, classNum,))
	return "Removed your class!"

# SocketIO
socketio = SocketIO(app)

listOfUsers = {}

@app.route("/chatbox")
def chatbox():
	return render_template('chatbox.html')

@socketio.on('set client')
def set_client(json):
	print(str(json))
	server_response(json['clientID'], request.sid)
	return 'one', 2

@socketio.on('my event')
def handle_custom_event(json):
	print('Received JSON: ' + str(json))
	#server_response(json['clientID'], request.sid)
	return 'one', 2

@socketio.on('to user message')
def send_user_msg(json):
	print(str(json))
	socketio.emit('user message', {'data': json['msg']}, room=listOfUsers[json['uid']])

def server_response(uid, sid):
	if int(uid) > 0:
		listOfUsers[uid] = sid
		print(listOfUsers)
		socketio.emit('server_response', {'data': uid}, room=sid)

if __name__ == "__main__":
	app.secret_key = "3sAmVAtdh!GNTSKuZJJn4^5wve"

	addDefaultAccounts()
	socketio.run(app, host='0.0.0.0')

# http://flask.pocoo.org/docs/0.12/quickstart/ #
