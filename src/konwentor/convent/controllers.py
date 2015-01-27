from sqlalchemy.orm.exc import NoResultFound
from pyramid.httpexceptions import HTTPNotFound

from hatak.controller import Controller

from .models import Convent
from .forms import ConventAddForm, ConventDeleteForm, ConventEditForm
from .helpers import ConventWidget


class ConventListController(Controller):

    template = 'convent:list.haml'
    permissions = [('base', 'view'), ]
    menu_highlighted = 'convent:list'

    def make(self):
        self.data['convents'] = self.get_convent_widgets()
        self.data['choosed_id'] = self.session.get('convent_id', None)

    def get_convent_widgets(self):
        return [
            ConventWidget(self.request, convent)
            for convent in self.get_convents()
        ]

    def get_convents(self):
        return self.query(Convent).filter_by(is_active=True).all()


class ConventAdd(Controller):

    template = 'convent:add.haml'
    permissions = [('convent', 'add'), ]
    menu_highlighted = 'convent:list'

    def make(self):
        form = self.add_form(ConventAddForm)

        if form.validate() is True:
            self.redirect('convent:list')


class ConventEditController(Controller):

    template = 'convent:edit.haml'
    permissions = [('convent', 'add'), ]
    menu_highlighted = 'convent:list'

    def make(self):
        convent = self.get_convent()

        form = self.add_form(ConventEditForm)
        form.set_value('id', convent.id)
        form.set_value('name', convent.name)

        if form.validate() is True:
            self.redirect('convent:list')

    def get_convent(self):
        try:
            obj_id = int(self.matchdict['obj_id'])
            self.data['convent'] = (
                self.query(Convent)
                .filter_by(id=obj_id, is_active=True)
                .one())
            return self.data['convent']
        except NoResultFound:
            raise HTTPNotFound()


class ConventDelete(Controller):
    template = 'convent:delete.haml'
    permissions = [('convent', 'delete'), ]
    menu_highlighted = 'convent:list'

    def make(self):
        self.verify_convent_id()

        form = self.add_form(ConventDeleteForm)
        form.set_value('obj_id', self.matchdict['obj_id'])

        if form.validate() is True:
            self.redirect('convent:list')

    def verify_convent_id(self):
        try:
            self.data['convent'] = (
                self.query(Convent)
                .filter_by(id=self.matchdict['obj_id'], is_active=True)
                .one())
        except NoResultFound:
            raise HTTPNotFound()


class ChooseConventController(ConventDelete):
    permissions = [('base', 'view'), ]

    def make(self):
        self.verify_convent_id()
        self.switch_convent()
        self.redirect('gamecopy:list')

    def switch_convent(self):
        self.session['convent_id'] = int(self.matchdict['obj_id'])
        for key in ['last_convent_id', 'last_user_id']:
            try:
                del(self.session[key])
            except KeyError:
                pass


class StartConventController(ChooseConventController):
    permissions = [('convent', 'add'), ]

    def make(self):
        self.verify_convent_id()
        self.switch_convent()
        self.start_convent()
        self.redirect('gamecopy:add')

    def start_convent(self):
        self.data['convent'].state = 'running'
        self.db.commit()


class EndConventController(ChooseConventController):
    permissions = [('convent', 'add'), ]

    def make(self):
        self.verify_convent_id()
        self.end_convent()
        self.redirect('convent:list')

    def end_convent(self):
        self.data['convent'].state = 'ended'
        self.db.commit()
