from konwentor.menu.base_controller import MenuController

from .models import Game


class GameListController(MenuController):

    renderer = 'game/list.jinja2'
    permissions = [('base', 'view'), ]
    menu_highlighted = 'game:list'

    def make(self):
        self.data['objects'] = self.get_games()

    def get_games(self):
        return self.db.query(Game).all()
