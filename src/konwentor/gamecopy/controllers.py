from sqlalchemy import and_
from hatak.controller import Controller

from konwentor.auth.models import User
from konwentor.convent.helpers import ConventWidget
from konwentor.convent.models import Convent
from konwentor.game.models import Game

from .forms import GameCopyAddForm
from .models import GameEntity, GameCopy
from .helpers import GameEntityWidget


class GameCopyControllerBase(Controller):

    def verify_convent(self):
        if 'convent_id' not in self.session:
            self.add_flashmsg('Proszę wybrać konwent.', 'danger')
            self.redirect('convent:list')
            return False
        return True

    def get_convent(self):
        return (
            self.query(Convent)
            .filter_by(id=self.session['convent_id'])
            .one())

    def make_helpers(self):
        super().make_helpers()
        self.add_helper('convent', ConventWidget, self.get_convent())


class GameCopyAddController(GameCopyControllerBase):

    template = 'gamecopy:add.jinja2'
    permissions = [('gamecopy', 'add'), ]
    menu_highlighted = 'gamecopy:add'

    def make(self):
        if not self.verify_convent():
            return

        form = self.add_form(GameCopyAddForm)
        initial_data = {
            'count': '1',
            'user_id': [str(self.user.id)],
            'convent_id': [str(self.session['convent_id'])]
        }

        if form(initial_data=initial_data):
            self.add_flashmsg('Dodano grę.', 'info')
            self.session['last_convent_id'] = form.get_value('convent_id')
            form.fields = {}
            form._gatherFormsData(initial_data)


class GameCopyListController(GameCopyControllerBase):

    template = 'gamecopy:list.haml'
    permissions = [('base', 'view'), ]
    menu_highlighted = 'gamecopy:list'

    def make(self):
        if not self.verify_convent():
            return

        self.data['convent'] = self.get_convent()
        self.data['games'] = [
            GameEntityWidget(self.request, obj) for obj
            in self.get_games(self.data['convent'])
        ]

    def get_games(self, convent):
        return (
            self.query(
                GameEntity,
                Game.name,
                User.name.label('author_name'))
            .join(GameCopy).join(Game).join(User)
            .filter(GameEntity.convent_id == convent.id)
            .all())


class GameCopyToBoxController(GameCopyControllerBase):

    permissions = [('gamecopy', 'add'), ]

    def make(self):
        if not self.verify_convent():
            return

        self.move_to_box()
        self.add_flashmsg('Gra została schowana.', 'success')
        self.redirect('gamecopy:list')

    def move_to_box(self):
        convent = self.get_convent()
        entity = self.get_game_entity(convent)
        entity.move_to_box()
        self.db.commit()

    def get_game_entity(self, convent):
        return (
            self.query(GameEntity)
            .filter(and_(
                GameEntity.convent_id == convent.id,
                GameEntity.id == self.matchdict['obj_id'],
            ))
            .one()
        )
