from konwentor.menu.base_controller import MenuController
from konwentor.forms.helpers import FormWidget

from .forms import GameCopyAddForm


class GameCopyAddController(MenuController):

    renderer = 'gamecopy/add.jinja2'
    permissions = [('gamecopy', 'add'), ]
    menu_highlighted = 'gamecopy:add'

    def make(self):
        self.form = GameCopyAddForm(self.request)
        self.form(initial_data={'user_id': [self.user.id]})

        # if self.form() is True:
        #     self.redirect('game:list')

    def make_helpers(self):
        super().make_helpers()
        self.add_helper('form', FormWidget, self.form)
