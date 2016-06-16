import handler

from entities import blog
from google.appengine.ext import db

class new_blog(handler.Handler):
	def render_front(self, subject="", content="", error=""):
		"""
			render page with the given conten
		"""
		self.render("new-blog.html", subject= subject, content= content, error=error, user_logged_in = self.user, user_name = self.user.username)

	def get(self):
		if self.user:
			self.render_front()
		else:
			self.redirect("/signup")

	def post(self):
		# get user input
		subject = self.request.get("subject")
		content = self.request.get("content")
		# get user id drom cookies
		user_id = self.read_secure_cookie('user_id')
		if user_id:
			if content and subject:
				# Add blog to the database
				new_blog = blog.Blog.add_blog(subject, content, user_id)
				new_blog.put()
				self.redirect("/blog/" + str(new_blog.key().id()))
			else:
				# missing fields alert user
				error = "we need both a subject and some content!"
				self.render_front(subject, content, error)
		else:
			self.redirect('/logout')