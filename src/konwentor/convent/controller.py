from konwentor.auth.base_controller import AuthController
from konwentor.application.helpers import FormWidget

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
        self.form = ConventAddForm(self.request)

        if self.form() is True:
            self.redirect('convent:list')

    def make_helpers(self):
        self.add_helper('form', FormWidget, self.form)
