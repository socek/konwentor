from hatak.controller import Controller

from .forms import GameCopyAddForm


class GameCopyAddController(Controller):

    renderer = 'gamecopy/add.jinja2'
    permissions = [('gamecopy', 'add'), ]
    menu_highlighted = 'gamecopy:add'

    def make(self):
        form = self.add_form(GameCopyAddForm)
        initial_data = {
            'count': '1',
            'user_id': [str(self.user.id)],
        }
        if form(initial_data=initial_data):
            self.add_flashmsg('Added game.', 'info')
            form()
