from pyramid.httpexceptions import HTTPForbidden
from hatak.controller import DatabaseController

from .models import User, NotLoggedUser


class AuthController(DatabaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.before.append(self.validate_auth)

    def validate_auth(self):
        self.user = self.get_user()
        if not self.user.has_access_to_controller(self):
            raise HTTPForbidden()

    def get_user(self):
        user_id = self.session.get('user_id', None)
        if user_id:
            return self.db.query(User).filter_by(id=user_id).one()
        else:
            return NotLoggedUser()

    def generate_default_data(self):
        data = super().generate_default_data()
        data['user'] = self.user
        self.user.assign_request(self.request)
        return data
