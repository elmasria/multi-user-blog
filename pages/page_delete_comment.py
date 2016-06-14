import handler
import helper

from google.appengine.ext import db

class delete(handler.Handler):
	def get(self, comment_id):
		if self.user:
			key = db.Key.from_path('comment', int(comment_id), parent=helper.comment_key())
			comment = db.get(key)
			user_id = self.read_secure_cookie('user_id')
			if comment.created_by == user_id:
				self.render("pre_delete_comment.html", comment = comment.comment_content, user_logged_in = self.user, user_name = self.user.username)
			else:
				self.render("not-allowed.html", not_allowed = True , base_page = "blog", requested_id = comment.post_id,  user_logged_in = self.user, user_name = self.user.username)
		else:
			self.redirect("/signup")

	def post(self, comment_id):
		key = db.Key.from_path('comment', int(comment_id), parent=helper.comment_key())
		comment = db.get(key)
		user_id = self.read_secure_cookie('user_id')
		if comment.created_by != user_id:
			self.render("not-allowed.html", requested_id = comment.post_id, base_page = "blog", user_logged_in = self.user, user_name = self.user.username)
		else:
			comment.delete()
			self.redirect("/success?delete_comment=true")