import handler


class success(handler.Handler):

    def get(self):
        message = "successfuly deleted"
        self.render("success.html",
                    message=message,
                    user_logged_in=self.user,
                    user_name=self.user.username)
