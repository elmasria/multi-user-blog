import helper

from google.appengine.ext import db

class comment(db.Model):
	comment_content = db.TextProperty(required = True)
	post_id = db.StringProperty(required = True)
	created_by = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty(auto_now_add = True)

	def get_content(self, s):
		return helper.return_valid_html(s)

	@classmethod
	def add_comment(cls, comment_content, post_id, created_by):
		return cls(parent = helper.comment_key(),
				   comment_content = comment_content,
				   post_id = post_id,
				   created_by = created_by)