from itsdangerous import URLSafeTimedSerializer
from flask.ext.mail import Message
from flask import *

from app import *

SECURITY_PASSWORD_SALT = '3sAmVAtdh!GNTSKuZJJn4^5wve'

def make_email_token(email):
    s = URLSafeTimedSerializer(SECURITY_PASSWORD_SALT)
    return s.dumps(email, salt=SECURITY_PASSWORD_SALT)

def confirm_email_token(token):
    print(token)
    s = URLSafeTimedSerializer(SECURITY_PASSWORD_SALT)
    print(s)
    try:
        email = s.loads(token, salt=SECURITY_PASSWORD_SALT, max_age=86400)
        print(email)
    except:
        return False
    return email

def send(to, token):
    html = render_template('activate.html', activationUrl=url_for('auth_activate', token=token, _external=True))
    msg = Message("Confirm Your QuickTutor Email", recipients=[to], html=html, sender="quicktutor@n8m8.us")
    print('boutta send')
    mail.send(msg)
    print('sent message')
