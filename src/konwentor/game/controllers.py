from sqlalchemy.orm.exc import NoResultFound
from pyramid.httpexceptions import HTTPNotFound
from hatak.controller import Controller

from .models import Game
from .forms import GameAddForm, GameDeleteForm


class GameListController(Controller):

    template = 'game:list.jinja2'
    permissions = [('base', 'view'), ]
    menu_highlighted = 'game:list'

    def make(self):
        self.data['objects'] = self.get_games()
        self.data['forms'] = {}
        self.add_game_forms()

    def get_games(self):
        return self.db.query(Game).filter_by(is_active=True).all()

    def add_game_forms(self):
        for game in self.data['objects']:
            name = 'form_%d' % (game.id)
            form = self.add_form(GameDeleteForm, name=name)
            self.data['forms'][game.id] = self.data[name]
            form.action = self.request.route_path(
                'game:delete', obj_id=game.id)
            form({
                'obj_id': [game.id, ],
            })


class GameAddController(Controller):

    template = 'game:add.jinja2'
    permissions = [('game', 'add'), ]
    menu_highlighted = 'game:list'

    def make(self):
        form = self.add_form(GameAddForm)

        if form() is True:
            self.redirect('game:list')


class GameDelete(Controller):
    template = 'game:delete.jinja2'
    permissions = [('game', 'delete'), ]
    menu_highlighted = 'game:list'

    def make(self):
        self.get_element()

        form = self.add_form(GameDeleteForm)
        form_data = {
            'obj_id': self.matchdict['obj_id'],
        }

        if form(form_data) is True:
            self.redirect('game:list')

    def get_element(self):
        try:
            self.data['element'] = (
                self.query(Game)
                .filter_by(id=self.matchdict['obj_id'])
                .one())
        except NoResultFound:
            raise HTTPNotFound()
