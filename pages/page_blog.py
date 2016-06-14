import handler
import helper

from entities import comment

from google.appengine.ext import db

class blog_by_id(handler.Handler):
	def get(self, blog_id):
		if self.user:
			key = db.Key.from_path('Blog', int(blog_id), parent=helper.blog_key())
			blog = db.get(key)

			comments = db.GqlQuery("select * from comment where post_id ='%s'order by created desc" % blog_id)

			if not blog:
				self.error(404)
				return
			if not comments:
				self.render("blog.html",  blog = blog, user_logged_in = self.user, user_name = self.user.username)
			else:
				self.render("blog.html", comments = comments,  blog = blog, user_logged_in = self.user, user_name = self.user.username)
		else:
			self.redirect("/signup")

	def post(self, blog_id):
		post_id = blog_id
		commentss = self.request.get("comment")
		user_id = self.read_secure_cookie('user_id')
		if user_id:
			if comment:
				new_comment = comment.comment.add_comment(commentss, post_id, user_id)
				new_comment.put()
				self.redirect("/blog/%s" % blog_id)
			else:
				key = db.Key.from_path('Blog', int(blog_id), parent=helper.blog_key())
				blog = db.get(key)
				error = "comment is required to submit new comment"
				self.render("blog.html", blog = blog, user_logged_in = self.user, user_name = self.user.username)
		else:
			self.redirect('/logout')