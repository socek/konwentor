from hatak.controller import Controller

from .forms import LoginForm
from .helpers import LoginFormWidget


class LoginController(Controller):

    template = 'auth:login.jinja2'

    def make(self):
        if self.user.is_logged():
            self.redirect('convent:list')
            return

        self.form = LoginForm(self.request)
        if self.form() is True:
            self.redirect('convent:list')

    def make_helpers(self):
        self.add_helper('form', LoginFormWidget, self.form)


class ForbiddenController(Controller):

    template = 'auth:forbidden.jinja2'

    def make(self):
        if not self.user.is_logged():
            self.redirect('auth:login')


class LogoutController(Controller):

    permissions = [('base', 'view'), ]

    def make(self):
        self.redirect('auth:login')
        self.session.clear()
