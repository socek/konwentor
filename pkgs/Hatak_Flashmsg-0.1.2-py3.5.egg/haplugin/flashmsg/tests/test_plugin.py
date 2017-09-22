from haplugin.toster import PluginTestCase, ControllerPluginTests, TestCase

from ..plugin import FlashMessagePlugin, FlashMessageControllerPlugin
from ..plugin import AddFlashmsgRequestPlugin
from ..helpers import FlashMessageWidget


class FlashMessagePluginTests(PluginTestCase):
    prefix_from = FlashMessagePlugin

    def test_add_controller_plugins(self):
        plugins = []
        self.plugin.add_controller_plugins(plugins)

        self.assertEqual([FlashMessageControllerPlugin], plugins)

    def test_add_request_plugins(self):
        self.add_mock_object(self.plugin, 'add_request_plugin')

        self.plugin.add_request_plugins()

        self.mocks['add_request_plugin'].assert_called_once_with(
            AddFlashmsgRequestPlugin)


class AddFlashmsgRequestPluginTests(TestCase):
    prefix_from = AddFlashmsgRequestPlugin

    def setUp(self):
        super().setUp()
        self.plugin = self.prefix_from()
        self.plugin.init(self.request)

    def test_call(self):
        """add_flashmsg should add flash message data to session"""
        self.request.session = {}

        self.plugin('message', 'type')

        self.assertEqual(
            [{'message': 'message', 'msgtype': 'type'}],
            self.request.session['flash_messages'])


class FlashMessageControllerPluginTests(ControllerPluginTests):
    prefix_from = FlashMessageControllerPlugin

    def test_make_helpers(self):
        self.add_mock_object(self.plugin, 'add_helper')

        self.plugin.make_helpers()

        self.mocks['add_helper'].assert_called_once_with(
            'flashmsg', FlashMessageWidget)
