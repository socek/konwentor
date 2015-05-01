from pytest import fixture, yield_fixture
from mock import patch, MagicMock

from haplugin.sql.testing import DatabaseFixture

from ..sidemenu import SideMenuWidget


class TestSideMenuWidget(DatabaseFixture):

    @fixture
    def widget(self, request):
        self.highlighted = 'highlited'
        widget = SideMenuWidget(request, self.highlighted)
        widget.data = {'menu': []}
        return widget

    @yield_fixture
    def MenuObject(self):
        patcher = patch(
            'konwentor.gameborrow.sidemenu.MenuObject',
            auto_spec=True
        )
        with patcher as mock:
            yield mock

    @yield_fixture
    def add_menu(self, widget):
        patcher = patch.object(widget, 'add_menu')
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

    def test_make(self, widget, mdriver, request, add_menu):
        convent = mdriver.Convent.get_convent_from_session.return_value
        convent.rooms = [MagicMock()]
        convent.rooms[0].name = 'My Room'

        widget.make()

        mdriver.Convent.get_convent_from_session.assert_called_once_with(
            request
        )
        add_menu.assert_called_once_with('My Room', None, 'star')
