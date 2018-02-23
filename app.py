from flask import Flask, render_template
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

# forgotPassword
@app.route("/auth/forgotpassword", methods=['POST'])
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
	return "notImplementedException"

# createlistings
@app.route("/request/respond", methods=['POST'])
def listings_respond():
	return "notImplementedException"


### Messages ###
# sendmessage
@app.route("/msg/send", methods=['POST'])
def msg_send():
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
	return "notImplementedException"

# AddClass
@app.route("/profile/addclass", methods=['POST'])
def profile_addclass():
	return "notImplementedException"

# RemoveClass
@app.route("/profile/removeclass", methods=['POST'])
def profile_removeclass():
	return "notImplementedException"

if __name__ == "__main__":
	app.run()

# http://flask.pocoo.org/docs/0.12/quickstart/ #
