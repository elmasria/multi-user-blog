import helper

from google.appengine.ext import db

class Blog(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created_by = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty(auto_now_add = True)

	def get_content(self, s):
		return helper.return_valid_html(s)

	def render(self):
		self._render_text = self.content.replace('\n', '<br>')
		return render_str("blog.html", p = self)

	@classmethod
	def add_blog(cls, subject, content, created_by):
		return cls(parent = helper.blog_key(),
				   subject = subject,
				   content = content,
				   created_by = created_by)