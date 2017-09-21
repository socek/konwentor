from pytest import yield_fixture
from mock import patch

from hatak.testing import PluginFixture, ControllerPluginFixture

from ..helpers import TopMenuWidget
from ..plugin import MenuPlugin, MenuControllerPlugin


class TestMenuPlugin(PluginFixture):
    prefix_from = MenuPlugin

    def _get_plugin_class(self):
        return MenuPlugin

    @yield_fixture
    def add_controller_plugin(self, plugin):
        with patch.object(plugin, 'add_controller_plugin') as mock:
            yield mock

    def test_add_controller_plugins(self, plugin, add_controller_plugin):
        """add_controller_plugins should add MenuControllerPlugin to plugins"""
        plugin.add_controller_plugins()

        add_controller_plugin.assert_called_once_with(MenuControllerPlugin)


class TestMenuControllerPlugin(ControllerPluginFixture):

    def _get_plugin_class(self):
        return MenuControllerPlugin

    def test_make_helpers_success(self, plugin, add_helper, controller):
        """
        make_helpers should add TopMenuWidget to helpers if
        controller.menu_highlighted is specyfied.
        """
        controller.menu_highlighted = 'something'

        plugin.make_helpers()

        add_helper.assert_called_once_with(
            'topmenu', TopMenuWidget, 'something')

    def test_make_helpers_fail(self, plugin, add_helper, controller):
        """
        make_helpers should do nothing if controller.menu_highlighted is not
        specyfied.
        """
        del(controller.menu_highlighted)

        plugin.make_helpers()
        assert not add_helper.called
