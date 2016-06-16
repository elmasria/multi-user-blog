import handler
import helper

from entities import comment
from entities import like

from google.appengine.ext import db


class blog_by_id(handler.Handler):

    def get(self, blog_id):
        # check if user is logged in
        if self.user:
            # user logged in
            # get blog by given id in the url
            key = db.Key.from_path(
                'Blog', int(blog_id), parent=helper.blog_key())
            blog = db.get(key)
            # get all like for the given blog
            likes_query = "select * from like where post_id='" + \
                blog_id + "'"
            likes = db.GqlQuery(likes_query)
            # get all comment for the given blog
            cmt_query = "select * from comment where post_id ='"+blog_id+"'"\
                "order by created desc"
            comments = db.GqlQuery(cmt_query)
            # check if blog exist in the database
            if not blog:
                self.error(404)
                return
            self.render("blog.html",
                        likes=likes.count(),
                        comments=comments,
                        blog=blog,
                        user_logged_in=self.user,
                        user_name=self.user.username)
        else:
            # user not looged in send user to signup page
            self.redirect("/signup")

    def post(self, blog_id):
        post_id = blog_id
        # get user input
        comments = self.request.get("comment")
        like_input = self.request.get("like")
        user_id = self.read_secure_cookie('user_id')
        # get old comments, likes and selected blog
        old_comments = db.GqlQuery("select * from comment " +
                                   "where post_id ='"+blog_id+"'" +
                                   "order by created desc")
        likes = db.GqlQuery("select * from like where post_id='"+blog_id+"'")
        key = db.Key.from_path('Blog', int(blog_id), parent=helper.blog_key())
        blog = db.get(key)
        # check if user is logged in
        if user_id:
            if comments:
                new_comment = comment.comment.add_comment(
                    comments, post_id, user_id)
                new_comment.put()
            if like_input:
                if user_id == blog.created_by:
                    error = "you can not like your post!"
                    self.render("blog.html",
                                error=error,
                                likes=likes.count(),
                                comments=old_comments,
                                blog=blog,
                                user_logged_in=self.user,
                                user_name=self.user.username)
                    return
                else:
                    # get likes for specific blog for the logged in user
                    user_likes_query = "select * from like " +\
                        "where post_id='"+blog_id + \
                        "' and created_by='"+str(self.user.key().id()) + "'"
                    check_user_likes = db.GqlQuery(user_likes_query)
                    if check_user_likes.count() == 0:
                        new_like = like.like.add_like(post_id, user_id)
                        new_like.put()
                    else:
                        error = "you can like a post one time"
                        self.render("blog.html",
                                    error=error,
                                    likes=likes.count(),
                                    comments=old_comments,
                                    blog=blog,
                                    user_logged_in=self.user,
                                    user_name=self.user.username)
                        return
            self.redirect("/blog/%s" % blog_id)
        else:
            self.redirect('/signup')
