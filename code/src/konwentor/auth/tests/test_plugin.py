from hatak.testing import ControllerPluginFixture

from ..plugin import AuthPluginControllerPlugin
from ..helpers import LinkWidget


class TestAuthPluginControllerPlugin(ControllerPluginFixture):

    def _get_plugin_class(self):
        return AuthPluginControllerPlugin

    def test_make_helpers(self, plugin, add_helper):
        """
        make_helpers should add LinkWidget widget
        """
        plugin.make_helpers()

        add_helper.assert_called_once_with(
            'link', LinkWidget)
