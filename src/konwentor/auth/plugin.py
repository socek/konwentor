from pyramid.httpexceptions import HTTPForbidden

from hatak.plugin import Plugin, RequestPlugin
from hatak.controller import ControllerPlugin

from .models import User, NotLoggedUser


class AuthPlugin(Plugin):

    def add_request_plugins(self):
        self.add_request_plugin(UserRequestPlugin)

    def add_unpackers(self, unpacker):
        unpacker.add('user', lambda req: req.user)

    def add_controller_plugins(self, plugins):
        plugins.append(AuthControllerPlugin)


class UserRequestPlugin(RequestPlugin):

    def __init__(self):
        super().__init__('user')

    def return_once(self):
        user_id = self.request.session.get('user_id', None)
        if user_id:
            return User.get_by_id(self.request.db, user_id)
        else:
            return NotLoggedUser()


class AuthControllerPlugin(ControllerPlugin):

    def before_filter(self):
        if not self.user.has_access_to_controller(self.controller):
            raise HTTPForbidden()

    def generate_default_data(self, data):
        data['user'] = self.user
        self.user.assign_request(self.request)
