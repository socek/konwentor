from sqlalchemy.orm.exc import NoResultFound
from pyramid.httpexceptions import HTTPNotFound

from hatak.controller import Controller

from .models import Convent
from .forms import ConventAddForm, ConventDeleteForm


class ConventListController(Controller):

    renderer = 'convent/list.jinja2'
    permissions = [('base', 'view'), ]
    menu_highlighted = 'convent:list'

    def make(self):
        self.data['convents'] = self.get_convents()
        self.data['choosed_id'] = self.session.get('convent_id', None)

    def get_convents(self):
        return self.db.query(Convent).all()


class ConventAdd(Controller):

    renderer = 'convent/add.jinja2'
    permissions = [('convent', 'add'), ]
    menu_highlighted = 'convent:list'

    def make(self):
        form = self.add_form(ConventAddForm)

        if form() is True:
            self.redirect('convent:list')


class ConventDelete(Controller):
    renderer = 'convent/delete.jinja2'
    permissions = [('convent', 'delete'), ]
    menu_highlighted = 'convent:list'

    def make(self):
        self.verify_convent_id()

        form = self.add_form(ConventDeleteForm)
        data = {
            'obj_id': self.matchdict['obj_id'],
        }

        if form(data) is True:
            self.redirect('convent:list')

    def verify_convent_id(self):
        try:
            self.data['convent'] = (
                self.query(Convent)
                .filter_by(id=self.matchdict['obj_id'])
                .one())
        except NoResultFound:
            raise HTTPNotFound()


class ChooseConventController(ConventDelete):
    permissions = [('base', 'view'), ]

    def make(self):
        self.verify_convent_id()
        self.session['convent_id'] = int(self.matchdict['obj_id'])
        self.redirect('convent:list')
