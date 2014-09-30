from haplugin.jinja2 import Jinja2HelperSingle

from .models import MenuObject


class MenuWidget(Jinja2HelperSingle):

    template = 'konwentor.menu:templates/main.jinja2'

    def __init__(self, request, highlighted):
        super().__init__(request)
        self.highlighted = highlighted

    def add_menu(self, *args, **kwargs):
        menu = MenuObject(self, *args, **kwargs)
        self.data['menu'].append(menu)
        return menu

    def make(self):
        self.data['menu'] = []
        self.add_menu('Konwenty', 'convent:list', 'calendar')
        self.add_menu('Gry', 'game:list', 'gamepad')

        submenu = self.add_menu('Na konwencie', None, 'star')
        submenu.add_child('Dodaj grę', 'gamecopy:add', 'magic')
        submenu.add_child('Lista gier', 'gamecopy:list', 'magic')
        submenu.add_child('Lista wypożyczeń', 'gameborrow:list', 'magic')
        submenu.add_child('Statystyki', 'statistics:all', 'magic')
