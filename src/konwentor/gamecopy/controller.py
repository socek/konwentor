from hatak.controller import Controller

from konwentor.forms.helpers import FormWidget

from .forms import GameCopyAddForm


class GameCopyAddController(Controller):

    renderer = 'gamecopy/add.jinja2'
    permissions = [('gamecopy', 'add'), ]
    menu_highlighted = 'gamecopy:add'

    def make(self):
        self.form = GameCopyAddForm(self.request)
        initial_data = {
            'count': '1',
            'user_id': [str(self.user.id)],
        }
        self.form(initial_data=initial_data)

        # if self.form() is True:
        #     pass
            # self.add_flashmsg('DONE!', 'danger')
        #     self.redirect('game:list')

    def make_helpers(self):
        super().make_helpers()
        self.add_helper('form', FormWidget, self.form)
