from hatak.plugins.plugin import Plugin
from hatak.controller import ControllerPlugin

from .helpers import MenuWidget


class MenuPlugin(Plugin):

    def add_controller_plugins(self, plugins):
        plugins.append(MenuControllerPlugin)


class MenuControllerPlugin(ControllerPlugin):

    def make_helpers(self):
        try:
            self.add_helper(
                'menu', MenuWidget, self.controller.menu_highlighted)
        except AttributeError:
            # if no menu_highlighted is avalible, it means no menu will be
            # needed
            pass
