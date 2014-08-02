from .base_controller import AuthController
from .forms import LoginForm


class LoginController(AuthController):

    renderer = 'auth/login.jinja2'

    def make(self):
        if self.user.is_logged():
            self.redirect('convent:home')
            return

        self.data['form'] = LoginForm(self.request)
        if self.data['form']() is True:
            self.redirect('convent:home')


class ForbiddenController(AuthController):

    renderer = 'auth/forbidden.jinja2'

    def make(self):
        if not self.user.is_logged():
            self.redirect('auth:login')
