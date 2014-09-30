from haplugin.toster import PluginTestCase, ControllerPluginTests

from ..plugin import FlashMessagePlugin, FlashMessageControllerPlugin
from ..helpers import FlashMessageWidget


class FlashMessagePluginTests(PluginTestCase):
    prefix_from = FlashMessagePlugin

    def test_add_controller_plugins(self):
        plugins = []
        self.plugin.add_controller_plugins(plugins)

        self.assertEqual([FlashMessageControllerPlugin], plugins)

    def test_after_config(self):
        self.plugin.after_config()

        self.config.add_request_method.assert_called_once_with(
            self.plugin.add_flashmsg,
            'add_flashmsg',
            reify=True)

    def test_add_flashmsg(self):
        """add_flashmsg should add flash message data to session"""
        self.request.session = {}
        add = self.plugin.add_flashmsg(self.request)

        add('message', 'type')

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
