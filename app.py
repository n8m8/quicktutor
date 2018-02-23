from flask import Flask, render_template
from pythonsql import *
app = Flask(__name__)

##### Front End Routes #####

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/test")
def test():
	return "test123"


##### Web Service Routes #####

### Authentication ###
# createAccount
@app.route("/auth/createaccount/<email>/<displayname>", methods=['POST'])
def auth_createAccount(email, displayname):
	password = request.form['password']
	return "notImplementedException"

# login
@app.route("/auth/login/<email>", methods=['POST'])
def auth_login(email):
	password = request.form['password']
	return "notImplementedException"

# forgotPassword
@app.route("/auth/forgotpassword/<email>", methods=['POST'])
def auth_forgotpassword():
	email = request.form['email']
	return "notImplementedException"


### Main Activity Page / Listings ###
# getlistings
@app.route("/listings/getall", methods=['GET'])
def listings_getall():
	return "notImplementedException"

# createlistings
@app.route("/listings/create/<email>/<location>/<cclass>/<description>", methods=['POST'])
def listings_create(email, location, cclass, description):
	return "notImplementedException"

# createlistings
@app.route("/request/respond/<email>/<listingId>", methods=['POST'])
def listings_respond(email, listingId):
	return "notImplementedException"


### Messages ###
# sendmessage
@app.route("/msg/send/<originId>/<destId>", methods=['POST'])
def msg_send(originId, destId):
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
@app.route("/profile/changescreenname/<newName>", methods=['POST'])
def profile_changescreenname(newName):
	return "notImplementedException"

# AddClass
@app.route("/profile/addclass/<classDept>/<classNum>", methods=['POST'])
def profile_addclass(classDept, classNum):
	return "notImplementedException"

# RemoveClass
@app.route("/profile/removeclass/<classDept>/<classNum>", methods=['POST'])
def profile_removeclass(classDept, classNum):
	return "notImplementedException"

if __name__ == "__main__":
	app.run()

# http://flask.pocoo.org/docs/0.12/quickstart/ #
