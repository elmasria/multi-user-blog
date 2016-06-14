import webapp2
from pages import page_home
from pages import page_create_blog
from pages import page_blog
from pages import page_signup
from pages import page_logout
from pages import page_login
from pages import page_edit_blog
from pages import page_delete_blog
from pages import page_success
from pages import page_edit_comment
from pages import page_delete_comment

app = webapp2.WSGIApplication([
	('/', page_home.main_page),
	('/newblog', page_create_blog.new_blog),
	('/blog/(\d+)', page_blog.blog_by_id),
	('/signup', page_signup.signup),
	('/logout', page_logout.logout),
	('/login', page_login.login),
	('/blog/edit/(\d+)', page_edit_blog.edit),
	('/blog/delete/(\d+)', page_delete_blog.delete),
	('/success', page_success.success),
	('/comment/edit/(\d+)', page_edit_comment.edit),
	('/comment/delete/(\d+)', page_delete_comment.delete)
	], debug=True)