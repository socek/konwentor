from hatak.plugins.toster.cases import TestCase
from ..helpers import MenuWidget


class MenuWidgetTests(TestCase):
    prefix_from = MenuWidget

    def setUp(self):
        super().setUp()
        self.highlited = 'highlited'
        self.widget = self.prefix_from(self.request, self.highlited)
        self.widget.data = {'menu': []}

    def test_init(self):
        self.assertEqual(self.highlited, self.widget.highlighted)

    def test_add_menu(self):
        """add_menu should create MenuObject and append it to the .data['menu']
        """
        self.add_mock('MenuObject', auto_spec=True)
        result = self.widget.add_menu('arg')

        self.assertEqual(self.mocks['MenuObject'].return_value, result)
        self.mocks['MenuObject'].assert_called_once_with(self.widget, 'arg')
        self.assertEqual(
            [result],
            self.widget.data['menu'])

    def test_make(self):
        """Sanity check."""
        self.widget.make()
