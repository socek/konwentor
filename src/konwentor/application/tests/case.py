from mock import MagicMock

from hatak.unpackrequest import unpack
from toster import TestCase as BaseTestCase

from konwentor.application.init import main
from konwentor.application.tests.runner import TestApplication


class TestCase(BaseTestCase):

    cache = {}

    def setUp(self):
        super().setUp()
        self.request = MagicMock()
        self.request.registry = {
            'db': MagicMock(),
            'unpacker': main.unpacker,
            'settings': {},
        }
        unpack(self, self.request)


class FormTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.form = self.prefix_from(self.request)


class ControllerTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.request.registry['controller_plugins'] = main.controller_plugins
        self.root_tree = MagicMock()
        self.controller = self.prefix_from(self.root_tree, self.request)


class SqlTestCase(TestCase):

    groups = ('sql',)

    def setUp(self):
        super().setUp()
        self.request.registry['db'] = TestApplication.get_db()
        unpack(self, self.request)


class SqlControllerTestCase(ControllerTestCase):

    groups = ('sql',)

    def setUp(self):
        super().setUp()
        self.request.registry['db'] = TestApplication.get_db()
        unpack(self, self.request)
        unpack(self.controller, self.request)
