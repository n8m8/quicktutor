from flask import Flask, render_template, request, redirect, session, jsonify, flash
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
listID = 0

##### Front End Routes #####

@app.route("/")
def index():
	if hasattr(session, 'logged_in'):
		if session['logged_in'] == True:
			return redirect('/dashboard')
		else:
			return render_template('index.html')
	else:
		return render_template('index.html')

@app.route("/test")
def test():
	return "test123"

@app.route("/dashboard")
def dashboard():
	print(session)
	if session['logged_in'] == True:
		flash("Logged In Successfully! ")
		return render_template('dashboard.html')
	else:
		return redirect('/')

@app.route("/TandC")
def terms():
    return render_template('TandC.html')


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
				flash("Almost done! Check your email to activate your account.")
				# return 'Almost done! Check your email to activate your account.'
			else:
				flash("Password did not meet strength requirements.")
				# return "Password did not meet strength requirements."
		else:
			flash("That email is already taken!")
			# return "That email is already taken!"
	else:
		flash("Invalid email address. Please use a valid @case.edu address.")
		# return "Invalid email address. Please use a valid @case.edu address."

	return render_template('index.html')

# activate
@app.route("/auth/activate/<token>", methods=['GET'])
def auth_activate(token):
	plaintextEmail = confirm_email_token(token)
	if plaintextEmail == False:
		flash("Invalid email activation token.")
		# return "Invalid email activation token."
	else:
		didConfirm = confirmUser((plaintextEmail,))
		if didConfirm == True:
			flash("Account successfully activated! Go log in.")
			# return "Account successfully activated! Go log in."
		else:
			flash("Unable to confirm user. Maybe your account is already activated, or your activation token expired.")
			# return "Unable to confirm user. Maybe your account is already activated, or your activation token expired."

	return render_template('index.html')


# forgotPassword
@app.route("/auth/forgotpassword", methods=['POST'])
def auth_forgotpassword():
	email = request.form['email']

	userid = getUserIdFromEmail((email,))
	if userid is None:
		flash("There is no account associated with that email address!")
		# return "There is no account associated with that email address!"
	else:
		newpassword = ""
		while len(newpassword) < 8:
			newpassword = newpassword + random.choice(string.ascii_letters + string.digits)
			changeUserPassword((generate_password_hash(newpassword), email,))

			flash("Your password was reset! Check your email for your new password.")

	return render_template('index.html')
			# return "Your password was reset! Check your email for your new password."


# Login
@app.route('/auth/login', methods=['POST'])
def login():
	# print(request.form)
	# userId = validateUserData((request.form['loginemail'], request.form['loginpassword'],))
	hashedPassword = getHashedPassword((request.form['loginemail'],))
	print(hashedPassword)
	print(request.form['loginemail'])
	if hashedPassword is None:
		# flash("There is no account associated with that email address.")
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
		flash("Login information was not valid.")
		return render_template('index.html')
		# return "Login information was not valid."

	return render_template('dashboard.html')

@app.route('/auth/logout', methods=['POST'])
def logout():
	# del socketIODict[request.cookies.get('session')]
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
		new['classname'] = getClassStringName((item[2],))
		new['shortDescription'] = item[3]
		new['topic'] = item[4]
		new['location'] = item[5]
		new['timestamp'] = item[6]
		ret.append(new)

	return json.dumps(ret)

# createlistings
@app.route("/listings/create", methods=['POST'])
def listings_create():
	className = request.form['newRequestClass']
	topic = request.form['newRequestTopic']
	location = request.form['newRequestLocation']
	description = request.form['newRequestDescription']
	classId = getClassIdFromName(className)
	addListing((session['user_name'], classId, description, topic, location,))
	message = {}
	message['className'] = className
	message['topic'] = topic
	message['location'] = location
	message['description'] = description
	message['userid'] = getUserIdFromEmail((session['user_name'],))
	socketio.emit('new listing', message, broadcast=True)
	flash("New request made successfully!")
	return render_template('dashboard.html') # i got an error when flashing w/o a return and this return is no content. actually might be because i'm not using a flask form when I make the request, i'm making a JQuery request

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
			flash("User did not exist")
			return "User did not exist"
	else:
		flash("Invalid protocol for this route, use GET")
		# return "Invalid protocol for this route, use GET"
	return render_template('dashboard.html')

# ChangeScreenName
@app.route("/profile/changescreenname", methods=['POST'])
def profile_changescreenname():
	newName = request.form['newName']
	changeUserScreenname((newName, session['user_name']))
	flash("Changed screennname!")
	return render_template('dashboard.html')
	# return "Changed screennname!"

# AddClass
@app.route("/profile/addclass", methods=['POST'])
def profile_addclass():
	classDept = request.form['classDept']
	classNum = request.form['classNum']
	addRuserClass((session['user_name'], classDept, classNum,))
	flash("Added your class!")
	return render_template('dashboard.html')
	# return "Added your class!"

# RemoveClass
@app.route("/profile/removeclass", methods=['POST'])
def profile_removeclass():
	classDept = request.form['classDept']
	classNum = request.form['classNum']
	deleteRuserClass((session['user_name'], classDept, classNum,))
	flash("Removed your class!")
	return render_template('dashboard.html')
	# return "Removed your class!"

@app.route("/profile/edit", methods=['POST'])
def profile_edit():
	addclasses = request.form['addclasses']
	deleteclasses = request.form['deleteclasses']
	screenname = request.form['screenname']

	for c in addclasses:
		addRuserclass((session['user_name'], c['classDept'], c['classNum']))

	for c in deleteclasses:
		deleteRuserClass((session['user_name'], c['classDept'], c['classNum']))

	flash("Updated your profile!")
	return render_template('dashboard.html')


@app.route("/listings/respond", methods=['POST'])
def listings_respond():
	email = session['user_name']
	listingId = request.form['listingId']
	requestingUserId = getUserIdFromListingId((listingId,))
	socketio.emit('tutor accepted', {'recipientUserId': requestingUserId})
	return ('', 204)

# SocketIO
socketio = SocketIO(app)

listOfUsers = {}
socketIODict = {}

@socketio.on('initConnection')
def init_connection(json):
	# sessionID = request.cookies.get('session')
	socketID = request.sid
	userID = getUserIdFromEmail((session['user_name'],))[0]
	print("INITING USER ID:", userID, session['user_name'])
	socketIODict[userID] = socketID;

@socketio.on('chat msg send')
def chat_msg_send(json):
	# sessionID = request.cookies.get('session')
	print("ROOM:", json['sioRoom'])
	sendMessageToRecipient(json['sioRoom'], json['message'])

def sendMessageToRecipient(recipientUserId, message):
	#connectedUserKeys = socketIODict.keys()
	#for key in connectedUserKeys:
	#	if sessionID != key:
	#		recvSessionID = key
	socketio.emit('chat msg recv', {'data': message}, room=recipientUserId)

@socketio.on('listing new')
def listing_new(json):
	print(json)
	userid = getUserIdFromEmail((session['user_name'],))
	print(userid)
	json['uid'] = userid[0]
	global listID
	json['lid'] = listID
	socketio.emit('listing broadcast', json, broadcast=True)
	listID += 1

@socketio.on('tutor accepted')
def tutor_accepted(json):
	#print('socketio on tutor accepted was executed')
	tutorid = getUserIdFromEmail((session['user_name'],))[0]
	userid = json['uid']
	print("USERID:", json['uid'], " TUTORID:", tutorid)
	sioTRoom = socketIODict[int(tutorid)]
	sioURoom = socketIODict[int(userid)]
	socketio.emit('chat msg init', {'roomid': sioTRoom}, room=sioURoom)
	socketio.emit('chat msg init', {'roomid': sioURoom}, room=sioTRoom)
	# DELETE LISTING USING GENERAL BROADCAST 

# METHOD FOR TUTOR CHATBOX HANDSHAKE
# After user accepts tutor request, this code runs
'''
	Chatbox is opened up on user with send location = tutor sessionID
	Chatbox is opened upon tutor with send location = user sessionID
	Messages are sent using same method, with destination = send location
'''

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
