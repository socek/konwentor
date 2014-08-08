from pyramid.httpexceptions import HTTPForbidden

from hatak.plugins.plugin import Plugin
from hatak.controller import ControllerPlugin

from .models import User, NotLoggedUser


class AuthPlugin(Plugin):

    def after_config(self):
        self.config.add_request_method(self.get_user, 'user', reify=True)

    def add_unpackers(self, unpacker):
        unpacker.add('user', lambda req: req.user)

    def get_user(self, request):
        session = request.session
        db = request.registry['db']

        user_id = session.get('user_id', None)
        if user_id:
            return db.query(User).filter_by(id=user_id).one()
        else:
            return NotLoggedUser()

    def add_controller_plugins(self, plugins):
        plugins.append(AuthControllerPlugin)


class AuthControllerPlugin(ControllerPlugin):

    def before_filter(self):
        if not self.user.has_access_to_controller(self.controller):
            raise HTTPForbidden()

    def generate_default_data(self, data):
        data['user'] = self.user
        self.user.assign_request(self.request)
