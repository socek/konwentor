from hatak.controller import Controller
from .helpers import UserWidget
from .forms import AuthEditForm, AuthAddForm
from .permissions import ListAvaliblePermissions


class AuthController(Controller):
    permissions = [('auth', 'edit'), ]

    def get_all_permissions_avalible(self, user=None):
        return ListAvaliblePermissions(self.request, user).get_all()


class AuthListController(AuthController):

    template = 'auth:list.haml'
    menu_highlighted = 'auth:list'

    def make(self):
        self.data['users'] = self.get_users()

    def get_users(self):
        for user in self.driver.Auth.find_all():
            yield UserWidget(self.request, user)


class AuthAddController(AuthController):
    permissions = [('auth', 'edit'), ]

    template = 'auth:add.haml'
    menu_highlighted = 'auth:list'

    def make(self):
        self.data['all_permissions'] = self.get_all_permissions_avalible()
        form = self.add_form(AuthAddForm)

        if form.validate():
            self.db.commit()
            self.add_flashmsg('Użytkownik został zapisany!', 'info')
            self.redirect('auth:list')


class AuthEditController(AuthController):

    template = 'auth:edit.haml'
    menu_highlighted = 'auth:list'

    def make(self):
        user = self.get_user()
        self.data['all_permissions'] = self.get_all_permissions_avalible(user)
        form = self.add_form(AuthEditForm)

        if form.validate():
            self.db.commit()
            self.add_flashmsg('Użytkownik został zapisany!', 'info')
            self.redirect('auth:list')
            return

        form.fill(user)

    def get_user(self):
        return self.driver.Auth.get_by_id(self.matchdict['obj_id'])
