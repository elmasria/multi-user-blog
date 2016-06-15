import helper

from google.appengine.ext import db

class like(db.Model):
	post_id = db.StringProperty(required = True)
	created_by = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

	@classmethod
	def add_like(cls, post_id, created_by):
		return cls(parent = helper.like_key(),
				   post_id = post_id,
				   created_by = created_by)