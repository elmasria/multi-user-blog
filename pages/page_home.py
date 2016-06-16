import webapp2
import handler

from entities import blog
from entities import users
from google.appengine.ext import db


class main_page(handler.Handler):
	def get(self):
		loged_in = False
		username = None
		blogs = blog.Blog.all().order('-created')
		if self.user:
			uid = self.read_secure_cookie('user_id')
			user = users.User.by_id(int(uid))
			loged_in = True
			username = user.username
		self.render("all-blogs.html", blogs = blogs, user_name = username , user_logged_in = loged_in)