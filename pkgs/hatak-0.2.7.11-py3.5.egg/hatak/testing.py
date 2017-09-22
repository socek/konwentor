from mock import MagicMock, patch
from pytest import fixture, yield_fixture

import hatak
from hatak.unpackrequest import unpack


class SessionDict(dict):

    def get_csrf_token(self):
        return MagicMock()


class ApplicatonFixture(object):

    @fixture(scope="session")
    def app(self):
        return hatak._test_cache['app']


class RequestFixture(ApplicatonFixture):

    def _get_default_request(self, app):
        request = MagicMock()
        request.registry = {
            'unpacker': app.unpacker,
            'settings': {},
            'paths': {},
        }
        return request

    @fixture
    def request(self, app, matchdict, session):
        request = self._get_default_request(app)
        request.matchdict = matchdict
        request.session = session
        unpack(self, request)
        return request

    @fixture
    def matchdict(self):
        return {}

    @fixture
    def session(self):
        return SessionDict()


class ControllerFixture(RequestFixture):

    def _get_controller_class(self):
        pass

    @fixture
    def root_tree(self):
        return MagicMock()

    @fixture
    def data(self):
        return {}

    @yield_fixture
    def redirect(self, controller):
        with patch.object(controller, 'redirect', autospec=True) as mock:
            yield mock

    @yield_fixture
    def add_helper(self, controller):
        with patch.object(controller, 'add_helper') as mock:
            yield mock

    @fixture
    def controller(self, app, request, root_tree, data):
        request.registry['controller_plugins'] = app.controller_plugins
        controller = self._get_controller_class()(root_tree, request)
        controller.data = data
        return controller


class PluginFixture(ApplicatonFixture):

    def _get_plugin_class(self):
        pass

    @fixture
    def fake_app(self):
        return MagicMock()

    @fixture
    def fake_config(self, fake_app):
        return fake_app.config

    @fixture
    def plugin(self, fake_app):
        plugin = self._get_plugin_class()()
        plugin.app = fake_app
        return plugin


class ControllerPluginFixture(ApplicatonFixture):

    def _get_plugin_class(self):
        pass

    @fixture
    def controller(self):
        return MagicMock()

    @fixture
    def parent(self):
        return MagicMock()

    @fixture
    def plugin(self, parent, controller):
        return self._get_plugin_class()(parent, controller)

    @yield_fixture
    def add_helper(self, plugin):
        with patch.object(plugin, 'add_helper') as mock:
            yield mock


class ModelFixture(RequestFixture):

    def _get_model_class(self):
        pass

    @fixture
    def model(self):
        return self._get_model_class()()
