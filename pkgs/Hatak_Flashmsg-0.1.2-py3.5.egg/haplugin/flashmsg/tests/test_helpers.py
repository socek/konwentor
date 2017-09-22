from haplugin.toster import TestCase

from ..helpers import FlashMessageWidget


class FlashMessageWidgetTests(TestCase):
    prefix_from = FlashMessageWidget

    def setUp(self):
        super().setUp()
        self.widget = FlashMessageWidget(self.request)
        self.session = self.widget.session = {}
        self.data = self.widget.data = {}

    def test_make(self):
        """FlashMessageWidget should get messages from session, and add it to
        templates."""
        self.add_mock('FlashMessage')
        data = {
            'message': 'message',
            'msgtype': 'type',
        }
        self.session['flash_messages'] = [data]

        self.widget.make()

        self.assertEqual([], self.session['flash_messages'])
        self.mocks['FlashMessage'].assert_called_once_with()
        obj = self.mocks['FlashMessage'].return_value
        obj.from_dict.assert_called_once_with(data)
        self.assertEqual([obj], self.data['messages'])
