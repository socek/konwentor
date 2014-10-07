from haplugin.toster import TestCase
from mock import MagicMock

from ..helpers import MenuWidget
from ..plugin import MenuPlugin, MenuControllerPlugin


class MenuPluginTests(TestCase):
    prefix_from = MenuPlugin

    def setUp(self):
        super().setUp()
        self.plugin = self.prefix_from()

    def test_add_controller_plugins(self):
        """add_controller_plugins should add MenuControllerPlugin to plugins"""
        self.add_mock_object(self.plugin, 'add_controller_plugin')

        self.plugin.add_controller_plugins()

        self.mocks['add_controller_plugin'].assert_called_once_with(
            MenuControllerPlugin)


class MenuControllerPluginTests(TestCase):
    prefix_from = MenuControllerPlugin

    def setUp(self):
        super().setUp()
        self.controller = MagicMock()
        self.parent = MagicMock()
        self.plugin = self.prefix_from(self.parent, self.controller)

    def test_make_helpers_success(self):
        """make_helpers should add MenuWidget to helpers if
        controller.menu_highlighted is specyfied."""
        self.add_mock_object(self.plugin, 'add_helper')
        self.controller.menu_highlighted = 'something'

        self.plugin.make_helpers()

        self.mocks['add_helper'].assert_called_once_with(
            'menu', MenuWidget, 'something')

    def test_make_helpers_fail(self):
        """make_helpers should do nothing if controller.menu_highlighted is not
        specyfied."""
        self.add_mock_object(self.plugin, 'add_helper')
        del(self.controller.menu_highlighted)

        self.plugin.make_helpers()
        self.assertEqual(0, self.mocks['add_helper'].call_count)
