from sqlalchemy.orm.exc import NoResultFound
from pyramid.httpexceptions import HTTPNotFound
from hatak.controller import Controller

from .forms import GameAddForm, GameDeleteForm, GameEditForm


class GameListController(Controller):

    template = 'game:list.jinja2'
    permissions = [('base', 'view'), ]
    menu_highlighted = 'game:list'

    def make(self):
        self.data['objects'] = self.get_games()
        self.data['forms'] = {}
        self.add_game_forms()

    def get_games(self):
        return self.driver.Game.get_actives().all()

    def add_game_forms(self):
        for game in self.data['objects']:
            name = 'form_%d' % (game.id)
            form = self.add_form(GameDeleteForm, name=name)
            self.data['forms'][game.id] = self.data[name]
            form.action = self.request.route_path(
                'game:delete', obj_id=game.id)
            form.set_value('obj_id', game.id)
            form.validate()


class GameEditController(Controller):

    template = 'game:edit.haml'
    permissions = [('game', 'add'), ]
    menu_highlighted = 'game:list'

    def make(self):
        form = self.add_form(GameEditForm)
        game = self.get_game()

        defaults = {}
        value_names = [
            'id',
            'name',
            'players_description',
            'time_description',
            'type_description',
            'difficulty']
        for name in value_names:
            defaults[name] = getattr(game, name) or ''
        form.parse_dict(defaults)

        if form.validate() is True:
            self.redirect('game:list')

    def get_game(self):
        try:
            obj_id = int(self.matchdict['obj_id'])
            self.data['game'] = self.driver.Game.get_active(obj_id)
            return self.data['game']
        except NoResultFound:
            raise HTTPNotFound()


class GameAddController(Controller):

    template = 'game:add.jinja2'
    permissions = [('game', 'add'), ]
    menu_highlighted = 'game:list'

    def make(self):
        form = self.add_form(GameAddForm)

        if form.validate() is True:
            self.redirect('game:list')


class GameDelete(Controller):
    template = 'game:delete.jinja2'
    permissions = [('game', 'delete'), ]
    menu_highlighted = 'game:list'

    def make(self):
        self.get_element()

        form = self.add_form(GameDeleteForm)
        form.set_value('obj_id', self.matchdict['obj_id'])

        if form.validate() is True:
            self.redirect('game:list')

    def get_element(self):
        try:
            self.data['element'] = self.driver.Game.get_active(
                self.matchdict['obj_id'])
        except NoResultFound:
            raise HTTPNotFound()
