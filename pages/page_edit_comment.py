import handler
import helper

from google.appengine.ext import db

class edit(handler.Handler):
	def get(self, comment_id):
		if self.user:
			key = db.Key.from_path('comment', int(comment_id), parent=helper.comment_key())
			comment = db.get(key)
			user_id = self.read_secure_cookie('user_id')
			if comment.created_by == user_id:
				self.render("edit-comment.html", comment= comment.comment_content, user_logged_in = self.user, user_name = self.user.username)
			else:
				# user not allowed to Edit other user comments
				self.render("not-allowed.html", not_allowed = True , base_page = "blog", requested_id = comment.post_id,  user_logged_in = self.user, user_name = self.user.username)
		else:
			self.redirect("/signup")

	def post(self, comment_id):
		key = db.Key.from_path('comment', int(comment_id), parent=helper.comment_key())
		comment = db.get(key)
		user_id = self.read_secure_cookie('user_id')
		if comment.created_by != user_id:
			# user not allowed to Edit other user comments
			self.render("not-allowed.html", not_allowed = True , base_page = "blog", requested_id = comment.post_id, user_logged_in = self.user, user_name = self.user.username)
		else:
			new_comment = self.request.get("comment")
			user_id = self.read_secure_cookie('user_id')
			if user_id:
				if new_comment:
					comment.comment_content = new_comment
					comment.put()
					self.redirect("/blog/%s" % comment.post_id)
				else:
					error = "Comment is required!"
					self.render("edit-comment.html", comment=comment.comment_content, error=error)
			else:
				self.redirect('/logout')