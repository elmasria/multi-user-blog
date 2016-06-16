import handler

from entities import users


class login(handler.Handler):

    def get(self):
        if self.user:
            self.redirect('/')
        else:
            self.render("login.html")

    def post(self):
        username_input = self.request.get('username')
        password_input = self.request.get('password')
        if username_input and password_input:
            u = users.User.login(username_input, password_input)
            if u:
                self.login(u)
                self.redirect('/')
            else:
                msg = 'Invalid login'
                self.render('login.html', error=msg)
        else:
            self.render("login.html",
                        username_error="Username Required",
                        password_error="Password Required")
