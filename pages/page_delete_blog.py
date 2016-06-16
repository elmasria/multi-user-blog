import handler
import helper

from google.appengine.ext import db


class delete(handler.Handler):

    def get(self, blog_id):
        if self.user:
            key = db.Key.from_path(
                'Blog', int(blog_id), parent=helper.blog_key())
            blog = db.get(key)
            user_id = self.read_secure_cookie('user_id')
            if blog.created_by == user_id:
                self.render("pre_delete_blog.html",
                            blog=blog,
                            subject=blog.subject,
                            content=blog.content,
                            user_logged_in=self.user,
                            user_name=self.user.username)
            else:
                # user not allowed to remove other user posts
                self.render("not-allowed.html",
                            not_allowed=True,
                            base_page="blog",
                            requested_id=blog_id,
                            user_logged_in=self.user,
                            user_name=self.user.username)
        else:
            self.redirect("/signup")

    def post(self, blog_id):
        key = db.Key.from_path('Blog', int(blog_id), parent=helper.blog_key())
        blog = db.get(key)
        user_id = self.read_secure_cookie('user_id')
        if blog.created_by != user_id:
            # user not allowed to remove other user posts
            self.render("not-allowed.html",
                        subject=blog.subject,
                        content=blog.content,
                        user_logged_in=self.user,
                        user_name=self.user.username)
        else:
            # remove blog and redirect user to the success page
            blog.delete()
            self.redirect("/success?delete_blog=true")
