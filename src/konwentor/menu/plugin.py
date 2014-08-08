from hatak.plugins.plugin import Plugin
from hatak.controller import ControllerPlugin

from .helpers import MenuWidget


class MenuPlugin(Plugin):

    def add_controller_plugins(self, plugins):
        plugins.append(MenuControllerPlugin)


class MenuControllerPlugin(ControllerPlugin):

    def make_helpers(self):
        self.add_helper('menu', MenuWidget, self.controller.menu_highlighted)
