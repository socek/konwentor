from pytest import fixture, yield_fixture
from mock import patch

from hatak.testing import RequestFixture

from ..helpers import MenuWidget


class TestMenuWidget(RequestFixture):

    @fixture
    def widget(self, request):
        self.highlighted = 'highlited'
        widget = MenuWidget(request, self.highlighted)
        widget.data = {'menu': []}
        return widget

    @yield_fixture
    def MenuObject(self):
        patcher = patch('konwentor.menu.helpers.MenuObject', auto_spec=True)
        with patcher as mock:
            yield mock

    def test_init(self, widget):
        assert widget.highlighted == self.highlighted

    def test_add_menu(self, widget, MenuObject):
        """
        add_menu should create MenuObject and append it to the .data['menu']
        """
        result = widget.add_menu('arg')

        assert result == MenuObject.return_value
        MenuObject.assert_called_once_with(widget, 'arg')
        assert widget.data['menu'] == [result]

    def test_make(self, widget):
        """Sanity check."""
        widget.make()
