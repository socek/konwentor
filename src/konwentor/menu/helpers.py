from haplugin.jinja2 import Jinja2HelperSingle

from .models import MenuObject


class OnConventMenuObject(MenuObject):

    def __init__(self, widget):
        super().__init__(widget, 'Na konwencie', None, 'star')

        self.add_child('Dodaj grę', 'gamecopy:add', 'magic')
        self.add_child('Lista gier', 'gamecopy:list', 'magic')
        self.add_child('Lista wypożyczeń', 'gameborrow:list', 'magic')
        self.add_child('Statystyki', 'statistics:all', 'magic')

    def is_avalible(self):
        return 'convent_id' in self.session


class TopMenuWidget(Jinja2HelperSingle):

    template = 'konwentor.menu:templates/main.jinja2'

    def __init__(self, request, highlighted):
        super().__init__(request)
        self.highlighted = highlighted

    def add_menu(self, *args, **kwargs):
        return self.add_menu_object(MenuObject(self, *args, **kwargs))

    def add_menu_object(self, menu):
        self.data['menu'].append(menu)
        return menu

    def make(self):
        self.data['menu'] = []
        self.add_menu('Konwenty', 'convent:list', 'calendar')
        self.add_menu('Gry', 'game:list', 'gamepad')

        self.add_menu_object(OnConventMenuObject(self))
