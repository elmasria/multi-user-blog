import handler
import helper

from entities import comment
from entities import like

from google.appengine.ext import db

class blog_by_id(handler.Handler):
	def get(self, blog_id):
		if self.user:
			key = db.Key.from_path('Blog', int(blog_id), parent=helper.blog_key())
			blog = db.get(key)
			likes = db.GqlQuery("select * from like where post_id='"+blog_id+"'")
			comments = db.GqlQuery("select * from comment where post_id ='%s'order by created desc" % blog_id)

			if not blog:
				self.error(404)
				return
			if not comments:
				self.render("blog.html",  blog = blog, user_logged_in = self.user, user_name = self.user.username)
			else:
				self.render("blog.html", likes= likes.count(), comments = comments,  blog = blog, user_logged_in = self.user, user_name = self.user.username)
		else:
			self.redirect("/signup")

	def post(self, blog_id):
		post_id = blog_id
		comments = self.request.get("comment")
		like_input = self.request.get("like")
		user_id = self.read_secure_cookie('user_id')
		old_comments = db.GqlQuery("select * from comment where post_id ='%s'order by created desc" % blog_id)
		likes = db.GqlQuery("select * from like where post_id='"+blog_id+"'")
		key = db.Key.from_path('Blog', int(blog_id), parent=helper.blog_key())
		blog = db.get(key)
		if user_id:
			if comments:
				new_comment = comment.comment.add_comment(comments, post_id, user_id)
				new_comment.put()
				#new_comments = db.GqlQuery("select * from comment where post_id ='%s'order by created desc" % blog_id)
				#self.redirect("/blog/%s" % blog_id)
				#self.render("blog.html", comments = new_comments, blog = blog, user_logged_in = self.user, user_name = self.user.username)
			if like_input:
				if user_id == blog.created_by:
					error = "you can not like your post!"
					self.render("blog.html", error=error, likes= likes.count(), comments = old_comments,  blog = blog, user_logged_in = self.user, user_name = self.user.username)
				else:
					check_user_likes = db.GqlQuery("select * from like where post_id='"+blog_id+"' and created_by='"+str(self.user.key().id()) +"'")
					if check_user_likes.count() == 0:
						new_like = like.like.add_like(post_id, user_id)
						new_like.put()
					else:
						error = "you can like your poste one time"
						self.render("blog.html", error=error, likes= likes.count(), comments = old_comments,  blog = blog, user_logged_in = self.user, user_name = self.user.username)
			#self.redirect("/blog/%s" % blog_id)
			# else:
			# 	key = db.Key.from_path('Blog', int(blog_id), parent=helper.blog_key())
			# 	blog = db.get(key)
			# 	error = "comment is required to submit new comment"
			# 	self.render("blog.html", comments = old_comments, blog = blog, user_logged_in = self.user, user_name = self.user.username)
		else:
			self.redirect('/logout')