from konwentor.auth.base_controller import AuthController

from .models import Convent
from .forms import ConventAddForm


class ConventListController(AuthController):

    renderer = 'convent/home.jinja2'
    permissions = [('base', 'view'), ]

    def make(self):
        self.data['convents'] = self.get_convents()

    def get_convents(self):
        return self.db.query(Convent).all()


class ConventAdd(AuthController):

    renderer = 'convent/add.jinja2'
    permissions = [('convent', 'add'), ]

    def make(self):
        self.data['form'] = ConventAddForm(self.request)
        if self.data['form']() is True:
            self.redirect('convent:list')
