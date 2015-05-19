from hatak.controller import Controller
from .helpers import UserWidget
from .forms import AuthEditForm


class AuthController(Controller):
    permissions = [('auth', 'edit'), ]


class AuthListController(AuthController):

    template = 'auth:list.haml'
    menu_highlighted = 'auth:list'

    def make(self):
        self.data['users'] = self.get_users()

    def get_users(self):
        for user in self.driver.Auth.find_all():
            yield UserWidget(self.request, user)


class AuthEditController(AuthController):

    template = 'auth:edit.haml'
    menu_highlighted = 'auth:list'

    def make(self):
        user = self.get_user()
        form = self.add_form(AuthEditForm)

        if form.validate():
            self.db.commit()
            self.add_flashmsg('Użytkownik został zapisany!', 'info')
            self.redirect('auth:list')
            return

        form.fill(user)

    def get_user(self):
        return self.driver.Auth.get_by_id(self.matchdict['obj_id'])
