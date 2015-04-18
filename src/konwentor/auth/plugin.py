from haplugin.auth.plugin import AuthPlugin
from hatak.controller import ControllerPlugin
from .helpers import LinkWidget


class KonwentorAuthPlugin(AuthPlugin):

    def add_controller_plugins(self):
        super().add_controller_plugins()
        self.add_controller_plugin(AuthPluginControllerPlugin)


class AuthPluginControllerPlugin(ControllerPlugin):

    def make_helpers(self):
        super().make_helpers()
        self.add_helper('link', LinkWidget)
