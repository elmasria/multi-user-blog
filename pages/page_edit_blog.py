import handler
import helper

from google.appengine.ext import db

class edit(handler.Handler):
	def get(self, blog_id):
		if self.user:
			key = db.Key.from_path('Blog', int(blog_id), parent=helper.blog_key())
			blog = db.get(key)
			user_id = self.read_secure_cookie('user_id')
			if blog.created_by == user_id:
				self.render("new-blog.html", subject= blog.subject, content= blog.content, user_logged_in = self.user, user_name = self.user.username)
			else:
				# user not allowed to Edit other user blogs
				self.render("not-allowed.html", not_allowed = True , base_page = "blog", requested_id = blog_id,  user_logged_in = self.user, user_name = self.user.username)
		else:
			self.redirect("/signup")

	def post(self, blog_id):
		key = db.Key.from_path('Blog', int(blog_id), parent=helper.blog_key())
		blog = db.get(key)
		user_id = self.read_secure_cookie('user_id')
		if blog.created_by != user_id:
			# user not allowed to Edit other user blogs
			self.render("not-allowed.html", subject= blog.subject, content= blog.content, user_logged_in = self.user, user_name = self.user.username)
		else:
			subject = self.request.get("subject")
			content = self.request.get("content")
			user_id = self.read_secure_cookie('user_id')
			if user_id:
				if content and subject:
					blog.subject = subject
					blog.content = content
					blog.put()
					self.redirect("/blog/%s" % blog_id)
				else:
					error = "we need both a subject and some content!"
					self.render_front(subject, content, error)
			else:
				self.redirect('/logout')