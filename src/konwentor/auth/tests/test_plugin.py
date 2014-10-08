from haplugin.toster import TestCase, ControllerPluginTests
from mock import MagicMock
from pyramid.httpexceptions import HTTPForbidden

from ..plugin import AuthPlugin, AuthControllerPlugin, UserRequestPlugin
from ..plugin import UserClassRequestPlugin


class AuthPluginTests(TestCase):
    prefix_from = AuthPlugin

    def setUp(self):
        super().setUp()
        self.app = MagicMock()
        self.plugin = AuthPlugin()
        self.plugin.init(self.app)

    def test_add_request_plugins(self):
        self.add_mock_object(self.plugin, 'add_request_plugin')

        self.plugin.add_request_plugins()

        self.assertEqual(2, self.mocks['add_request_plugin'].call_count)
        self.mocks['add_request_plugin'].assert_any_call(UserRequestPlugin)
        self.mocks['add_request_plugin'].assert_any_call(
            UserClassRequestPlugin)

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
        self.plugin.app.unpacker = unpacker
        self.plugin.add_unpackers()
        self.assertEqual(True, cache['runned'])

    def test_add_controller_plugins(self):
        self.add_mock_object(self.plugin, 'add_controller_plugin')

        self.plugin.add_controller_plugins()

        self.mocks['add_controller_plugin'].assert_called_once_with(
            AuthControllerPlugin)


class UserRequestPluginTests(TestCase):
    prefix_from = UserRequestPlugin

    def setUp(self):
        super().setUp()
        self.parent = MagicMock()
        self.plugin = self.prefix_from()
        self.plugin.set_parent(self.parent)
        self.plugin.init(self.request)

    def test_get_user(self):
        """get_user should get user_id from session and return User object with
        the same id"""
        self.request.session = {
            'user_id': 100,
        }
        self.parent.User.get_by_id.reset_mock()

        result = self.plugin.return_once()

        self.assertEqual(
            self.parent.User.get_by_id.return_value,
            result)
        self.parent.User.get_by_id.assert_called_once_with(self.db, 100)

    def test_get_user_fake(self):
        """get_user should return NotLoggedUser object if no user_id found in
        session"""
        self.request.session = {}

        result = self.plugin.return_once()

        self.assertEqual(self.parent.NotLoggedUser.return_value, result)


class UserClassRequestPluginTests(TestCase):
    prefix_from = UserClassRequestPlugin

    def setUp(self):
        super().setUp()
        self.parent = MagicMock()
        self.plugin = self.prefix_from()
        self.plugin.set_parent(self.parent)
        self.plugin.init(self.request)

    def test_return_once(self):
        self.assertEqual(self.parent.User, self.plugin.return_once())


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
