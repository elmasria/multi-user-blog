import webapp2
from pages import page_home
from pages import page_create_blog
from pages import page_blog
from pages import page_signup
from pages import page_logout
from pages import page_login

app = webapp2.WSGIApplication([
	('/', page_home.main_page),
	('/newblog', page_create_blog.new_blog),
	('/blog/(\d+)', page_blog.blog_by_id),
	('/signup', page_signup.signup),
	('/logout', page_logout.logout),
	('/login', page_login.login)
	], debug=True)