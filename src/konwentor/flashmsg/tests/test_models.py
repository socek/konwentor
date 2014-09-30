from haplugin.toster import TestCase

from ..models import FlashMessage


class FlashMessageTests(TestCase):
    prefix_from = FlashMessage

    def setUp(self):
        super().setUp()
        self.model = FlashMessage('message', 'type')

    def test_init(self):
        self.assertEqual('message', self.model.message)
        self.assertEqual('type', self.model.msgtype)

    def test_to_dict(self):
        self.assertEqual({
            'message': 'message',
            'msgtype': 'type',
        }, self.model.to_dict())

    def test_from_dict(self):
        self.model.from_dict({
            'message': 'message2',
            'msgtype': 'type2',
        })

        self.assertEqual('message2', self.model.message)
        self.assertEqual('type2', self.model.msgtype)
