from hatak.controller import Controller

from konwentor.convent.models import Convent
from konwentor.game.models import Game
from konwentor.auth.models import User

from .forms import GameCopyAddForm
from .models import GameCopyOnConvent, GameCopy


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


class GameCopyAddController(GameCopyControllerBase):

    renderer = 'gamecopy/add.jinja2'
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

    renderer = 'gamecopy/list.jinja2'
    permissions = [('base', 'view'), ]
    menu_highlighted = 'gamecopy:list'

    def make(self):
        if not self.verify_convent():
            return

        self.data['convent'] = self.get_convent()
        self.data['games'] = self.get_games(self.data['convent'])

    def get_games(self, convent):
        return (
            self.query(
                GameCopyOnConvent.count,
                Game.name,
                User.name.label('author_name'))
            .join(GameCopy).join(Game).join(User)
            .filter(GameCopyOnConvent.convent_id == convent.id)
            .all())
