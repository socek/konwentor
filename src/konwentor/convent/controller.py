from konwentor.auth.base_controller import AuthController
from konwentor.application.helpers import FormWidget

from .models import Convent
from .forms import ConventAddForm, ConventDeleteForm


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


class ConventDelete(AuthController):
    renderer = 'convent/delete.jinja2'
    permissions = [('convent', 'delete'), ]

    def make(self):
        obj_id = self.matchdict['obj_id']
        self.data['convent'] = (
            self.db.query(Convent).filter_by(id=obj_id).one())

        self.form = ConventDeleteForm(self.request)
        form_data = {
            'obj_id': obj_id,
        }

        if self.form(form_data) is True:
            self.redirect('convent:list')

    def make_helpers(self):
        self.add_helper('form', FormWidget, self.form)
