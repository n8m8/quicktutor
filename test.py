import unittest
from flask.ext.testing import TestCase
# from flask_testing import TestCase
import app as ap
# from app import index, test, dashboard, terms, request_submitTestForm, auth_signup, auth_activate, auth_forgotpassword, login, logout, request_getUserInfo, listings_getall, listings_create, profile_get, profile_changescreenname, profile_addclass, profile_removeclass, profile_edit, listings_respond, init_connection, chat_msg_send, sendMessageToRecipient, tutor_accepted, chatbox, set_client, handle_custom_event, send_user_msg, server_response

class MyTest(TestCase):

	def create_app(self):
		return ap.app

	def test_index(self):
		self.client.get('/')
		self.assert_template_used('index.html')

	def test_test(self):
		self.client.get('/test')
		self.assertTrue(ap.test() == "test123")

	# def test_dashboard(self):
		# self.client.get('/dashboard')
		# self.assert_template_used('dashboard.html')
	def test_signup(self):
		resp = self.client.get('/auth/signup')
		# Ensure that valid fields result in success.
		resp = self.client.post('auth/signup', {
		'signupemail': 'qtadmin@case.edu',
		'signuppassword': 'Password1',
		}, follow_redirects=False)
		self.assertEqual(resp.status_code, 302)




	def test_request_getUserInfo(self):
		response = self.i.get("/request/getUserInfo")
		data = json.loads(response.get_data(as_text=True))
		self.assertEqual(data['userid', 'email', 'password', 'displayname'], 1, "test@case.edu", "password", "TestUser")

	#test if flask was set up correctly
	def test_index(self):
		tester = app.test_client(self)
		response = tester.get('/login', context_type = 'html/text')
		self.assertEqual(response.status_code, 200)


if __name__== '__main__':
	unittest.main()

from flask import Flask
from flask_testing import LiveServerTestCase

class MyTest(LiveServerTestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        # Default port is 5000
        app.config['LIVESERVER_PORT'] = 5000
        # Default timeout is 5 seconds
        app.config['LIVESERVER_TIMEOUT'] = 10
        return app

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)
