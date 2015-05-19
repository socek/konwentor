from haplugin.auth.plugin import AuthPlugin
from hatak.controller import ControllerPlugin
from .helpers import LinkWidget

from .driver import KonwentorAuthDriver


class KonwentorAuthPlugin(AuthPlugin):

    def add_controller_plugins(self):
        super().add_controller_plugins()
        self.add_controller_plugin(AuthPluginControllerPlugin)

    def generate_drivers(self, sql):
        sql.add_group(KonwentorAuthDriver(self.User))


class AuthPluginControllerPlugin(ControllerPlugin):

    def make_helpers(self):
        super().make_helpers()
        self.add_helper('link', LinkWidget)
