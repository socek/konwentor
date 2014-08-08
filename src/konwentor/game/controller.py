from sqlalchemy.orm.exc import NoResultFound
from pyramid.httpexceptions import HTTPNotFound
from hatak.controller import Controller

from konwentor.forms.helpers import FormWidget

from .models import Game
from .forms import GameAddForm, GameDeleteForm


class GameListController(Controller):

    renderer = 'game/list.jinja2'
    permissions = [('base', 'view'), ]
    menu_highlighted = 'game:list'

    def make(self):
        self.data['objects'] = self.get_games()

    def get_games(self):
        return self.db.query(Game).all()


class GameAddController(Controller):

    renderer = 'game/add.jinja2'
    permissions = [('game', 'add'), ]
    menu_highlighted = 'game:list'

    def make(self):
        self.form = GameAddForm(self.request)

        if self.form() is True:
            self.redirect('game:list')

    def make_helpers(self):
        super().make_helpers()
        self.add_helper('form', FormWidget, self.form)


class GameDelete(Controller):
    renderer = 'game/delete.jinja2'
    permissions = [('game', 'delete'), ]
    menu_highlighted = 'game:list'

    def make(self):
        self.get_element()

        self.form = GameDeleteForm(self.request)
        form_data = {
            'obj_id': self.matchdict['obj_id'],
        }

        if self.form(form_data) is True:
            self.redirect('game:list')

    def get_element(self):
        try:
            self.data['element'] = (
                self.query(Game)
                .filter_by(id=self.matchdict['obj_id'])
                .one())
        except NoResultFound:
            raise HTTPNotFound()

    def make_helpers(self):
        super().make_helpers()
        self.add_helper('form', FormWidget, self.form)
