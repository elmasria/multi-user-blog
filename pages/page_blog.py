import handler
import helper

from google.appengine.ext import db

class blog_by_id(handler.Handler):
	def get(self, blog_id):
		if self.user:
			#blog = Blog.get_by_id(int(blog_id))
			key = db.Key.from_path('Blog', int(blog_id), parent=helper.blog_key())
			blog = db.get(key)

			if not blog:
				self.error(404)
				return

			self.render("blog.html", blog = blog, user_logged_in = self.user, user_name = self.user.username)
		else:
			self.redirect("/signup")