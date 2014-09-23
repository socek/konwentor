from hatak.plugins.toster.cases import TestCase, ControllerPluginTests
from mock import MagicMock
from pyramid.httpexceptions import HTTPForbidden

from ..plugin import AuthPlugin, AuthControllerPlugin


class AuthPluginTests(TestCase):
    prefix_from = AuthPlugin

    def setUp(self):
        super().setUp()
        self.app = MagicMock()
        self.plugin = AuthPlugin()
        self.plugin.init(self.app)

    def test_after_config(self):
        self.plugin.after_config()

        self.app.config.add_request_method.assert_called_once_with(
            self.plugin.get_user, 'user', reify=True)

    def test_add_unpackers(self):
        cache = {'runned': False}

        def unpacker_add(name, method):
            cache['runned'] = True
            self.assertEqual('user', name)
            req = MagicMock()
            result = method(req)
            self.assertEqual(req.user, result)
        unpacker = MagicMock()
        unpacker.add = unpacker_add
        self.plugin.add_unpackers(unpacker)
        self.assertEqual(True, cache['runned'])

    def test_add_controller_plugins(self):
        plugins = []
        self.plugin.add_controller_plugins(plugins)

        self.assertEqual([AuthControllerPlugin], plugins)

    def test_get_user(self):
        """get_user should get user_id from session and return User object with
        the same id"""
        self.request.session = {
            'user_id': 100,
        }
        self.add_mock('User')

        result = self.plugin.get_user(self.request)

        self.assertEqual(
            self.mocks['User'].get_by_id.return_value,
            result)
        self.mocks['User'].get_by_id.assert_called_once_with(self.db, 100)

    def test_get_user_fake(self):
        """get_user should return NotLoggedUser object if no user_id found in
        session"""
        self.request.session = {}
        self.add_mock('NotLoggedUser')

        result = self.plugin.get_user(self.request)

        self.assertEqual(self.mocks['NotLoggedUser'].return_value, result)


class AuthControllerPluginTests(ControllerPluginTests):
    prefix_from = AuthControllerPlugin

    def test_before_filter(self):
        """before_filter should do nothing, when user has access to controller
        """
        self.plugin.user = MagicMock()
        self.plugin.user.has_access_to_controller.return_value = True

        self.plugin.before_filter()

        self.plugin.user.has_access_to_controller.assert_called_once_with(
            self.controller)

    def test_before_filter_raises(self):
        """before_filter should raises HTTPForbidden when use has no access
        to controller
        """
        self.plugin.user = MagicMock()
        self.plugin.user.has_access_to_controller.return_value = False

        self.assertRaises(HTTPForbidden, self.plugin.before_filter)

        self.plugin.user.has_access_to_controller.assert_called_once_with(
            self.controller)

    def test_generate_default_data(self):
        data = {}
        self.plugin.user = MagicMock()
        self.plugin.generate_default_data(data)

        self.assertEqual(self.plugin.user, data['user'])

        self.plugin.user.assign_request.assert_called_once_with(
            self.controller.request)

