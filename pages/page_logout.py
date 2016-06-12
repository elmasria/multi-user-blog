import helper
import handler

class logout(handler.Handler):
    def get(self):
        self.logout()
        self.redirect('/signup')