import random
import string
import hashlib
import hmac

from string import letters
from google.appengine.ext import db

SecurityCode = "SecuredUdacityPassword"


def blog_key(name = 'default'):
	return db.Key.from_path('blogs', name)


def user_key(name = 'default'):
	return db.Key.from_path('users', name)


def make_salt():
	return ''.join(random.choice(string.letters) for x in xrange(5))

def hash_password(name, pw, slt = None):
	salt = slt or make_salt()
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
	return hash_password(name, pw, h.split("|")[1]) == h

def return_valid_html(s):
	return s.replace('\n', '<br>')

def make_secure_val(val):
	return '%s|%s' % (val, hmac.new(SecurityCode, val).hexdigest())

def check_secure_val(secure_val):
	# get the original value
	val = secure_val.split('|')[0]
	# check if the value is valid
	if secure_val == make_secure_val(val):
		# return valid value
		return val