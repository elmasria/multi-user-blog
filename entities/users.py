import helper

from google.appengine.ext import db

class User(db.Model):
	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	email = db.StringProperty(required = False)
	created = db.DateTimeProperty(auto_now_add = True)

	@classmethod
	def by_id(cls, uid):
		return cls.get_by_id(uid, parent = helper.user_key())

	@classmethod
	def by_name(cls, name):
		u = cls.all().filter('username =', name).get()
		return u

	@classmethod
	def register(cls, name, pw, email = None):
		pw_hash = helper.hash_password(name, pw)
		return cls(parent = helper.user_key(),
				   username = name,
				   password = pw_hash,
				   email = email)

	@classmethod
	def login(cls, name, pw):
		u = cls.by_name(name)
		if u and helper.valid_pw(name, pw, u.password):
			return u