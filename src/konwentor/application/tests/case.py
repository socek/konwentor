from mock import MagicMock

from toster import TestCase as BaseTestCase

from konwentor.application.init import main


class TestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.request = MagicMock()
        self.request.registry = {
            'db': MagicMock(),
            'unpacker': main.unpacker,
            'settings': {}}
        self.db = self.request.registry['db']


class FormTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.form = self.prefix_from(self.request)
