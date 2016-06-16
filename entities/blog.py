import helper

from google.appengine.ext import db


class Blog(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created_by = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now_add=True)

    def get_content(self, s):
        """
                Return a valid HTML by
                replacing the new line "\n" by "<br>"
        """
        return helper.return_valid_html(s)

    @classmethod
    def add_blog(cls, subject, content, created_by):
        """
                Return Blog object with the given input
        """
        return cls(parent=helper.blog_key(),
                   subject=subject,
                   content=content,
                   created_by=created_by)
