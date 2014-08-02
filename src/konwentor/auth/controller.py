from .base_controller import AuthController
from .forms import LoginForm


class LoginController(AuthController):

    renderer = 'auth/login.jinja2'

    def make(self):
        if self.user.is_logged():
            self.redirect('convent:list')
            return

        self.data['form'] = LoginForm(self.request)
        if self.data['form']() is True:
            self.redirect('convent:list')


class ForbiddenController(AuthController):

    renderer = 'auth/forbidden.jinja2'

    def make(self):
        if not self.user.is_logged():
            self.redirect('auth:login')


class LogoutController(AuthController):

    permissions = [('base', 'view'), ]

    def make(self):
        self.redirect('auth:login')
        self.session.clear()
