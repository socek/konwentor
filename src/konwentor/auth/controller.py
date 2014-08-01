from .base_controller import AuthController


class LoginController(AuthController):

    renderer = 'auth/login.jinja2'
