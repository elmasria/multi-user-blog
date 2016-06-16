import handler
import re
import helper
from entities import users

SecurityCode = "SecuredUdacityPassword"

rg_exp_username = re.compile("^[a-zA-Z0-9_-]{3,20}$")
reg_exp_pass = re.compile("^.{3,20}$")
regular_exp_email = re.compile("^[\S]+@[\S]+.[\S]+$")


class signup(handler.Handler):

    def register_user(self, un, pw, em):
        u = users.User.by_name(un)
        if u:
            msg = 'user already exists.'
            self.render('signup.html', username_error=msg)
        else:
            new_user = users.User.register(un, pw, em)
            new_user.put()
            self.login(new_user)
            self.redirect('/')

    def get(self):
        if self.user:
            self.redirect('/')
        else:
            self.render("signup.html")

    def post(self):
        # get user input
        username_input = self.request.get('username')
        password_input = self.request.get('password')
        verify_input = self.request.get('verify')
        email_input = self.request.get('email')

        reg_ex_name = rg_exp_username.match(username_input)
        reg_ex_pass = reg_exp_pass.match(password_input)

        # check if input is valid (Required fields, match regular expressions)
        if username_input and password_input and verify_input:
            if reg_ex_name and reg_ex_pass:
                if password_input == verify_input:
                    if email_input:
                        if regular_exp_email.match(email_input):
                            # register user
                            self.register_user(
                                username_input, password_input, email_input)
                        else:
                            self.render("signup.html",
                                        username=username_input,
                                        email=email_input,
                                        email_error="Invalid Email")
                    else:
                        # register user
                        self.register_user(
                            username_input, password_input, email_input)
                else:
                    self.render("signup.html",
                                username=username_input,
                                email=email_input,
                                verify_error="Password doesn't match")
            else:
                self.render("signup.html",
                            username=username_input,
                            email=email_input,
                            username_error="Invalid Username",
                            password_error="Invalid Password")
        else:
            self.render("signup.html",
                        username_error="Username Required",
                        password_error="Password Required")
