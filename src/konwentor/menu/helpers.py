from hatak.plugins.jinja2 import Jinja2Helper

from .models import MenuObject


class MenuWidget(Jinja2Helper):

    template = 'menu/main.jinja2'

    def __init__(self, request, highlighted):
        super().__init__(request)
        self.highlighted = highlighted

    def add_menu(self, *args, **kwargs):
        self.data['menu'].append(MenuObject(self, *args, **kwargs))

    def make(self):
        self.data['menu'] = []
        self.add_menu('Konwenty', 'convent:list', 'calendar')
        self.add_menu('Gry', 'game:list', 'gamepad')
