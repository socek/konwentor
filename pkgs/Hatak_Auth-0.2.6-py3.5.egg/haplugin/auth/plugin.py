from pyramid.httpexceptions import HTTPForbidden
from pyramid.exceptions import Forbidden

from hatak.plugin import Plugin, RequestPlugin
from hatak.controller import ControllerPlugin
from haplugin.jinja2 import Jinja2Plugin
from haplugin.sql import SqlPlugin

from .models import User, NotLoggedUser
from .driver import AuthDriver


class AuthPlugin(Plugin):

    User = User
    NotLoggedUser = NotLoggedUser

    def add_request_plugins(self):
        self.add_request_plugin(UserRequestPlugin)
        self.add_request_plugin(UserClassRequestPlugin)

    def add_unpackers(self):
        self.unpacker.add('user', lambda req: req.user)

    def add_controller_plugins(self):
        self.add_controller_plugin(AuthControllerPlugin)

    def append_routes(self):
        self.route.prefix = 'haplugin.'
        self.route.add(
            'auth.controllers.LoginController',
            'auth:login',
            '/login')
        self.route.add(
            'auth.controllers.LogoutController',
            'auth:logout',
            '/logout')
        self.route.add_view(
            'auth.controllers.ForbiddenController',
            context=Forbidden)

    def validate_plugin(self):
        self.app._validate_dependency_plugin(Jinja2Plugin)
        self.app._validate_dependency_plugin(SqlPlugin)

    def generate_drivers(self, sql):
        sql.add_group(AuthDriver(self.User))


class UserRequestPlugin(RequestPlugin):

    def __init__(self):
        super().__init__('user')

    def return_once(self):
        user_id = self.request.session.get('user_id', None)
        if user_id:
            try:
                return self.driver.Auth.get_by_id(user_id)
            except:
                pass
        return self.parent.NotLoggedUser()


class UserClassRequestPlugin(RequestPlugin):

    def __init__(self):
        super().__init__('user_cls')

    def return_once(self):
        return self.parent.User


class AuthControllerPlugin(ControllerPlugin):

    def before_filter(self):
        if not self.user.has_access_to_controller(self.controller):
            raise HTTPForbidden()

    def generate_default_data(self, data):
        data['user'] = self.user
        self.user.assign_request(self.request)
