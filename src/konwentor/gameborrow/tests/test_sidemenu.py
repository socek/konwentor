from pytest import fixture, yield_fixture
from mock import patch, MagicMock, call

from haplugin.sql.testing import DatabaseFixture

from ..sidemenu import SideMenuWidget, RoomMenuObject


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
        add_menu.assert_has_calls([
            #call('My Room', None, 'star'),
            call('Misc', None, 'star'),
        ])


class TestRoomMenuObject(DatabaseFixture):

    @fixture
    def widget(self, request):
        widget = MagicMock()
        widget.request = request
        widget.highlighted = 'route2'
        return widget

    @fixture
    def model(self, widget):
        self.name = 'name'
        self.rotue = 'route'
        self.icon = 'icon'
        return RoomMenuObject(
            widget,
            self.name,
            self.route,
            self.icon,
            'arg',
            kw='arg'
        )

    def test_get_room_id_when_exists(self, model):
        """
        get_room_id should return room_id from route args
        """
        model.route_args[1]['room_id'] = 10
        assert model.get_room_id() == 10

    def test_get_room_id_when_not_exists(self, model):
        """
        get_room_id should return None if no room_id in route args
        """
        assert model.get_room_id() == None

    def test_is_highlited_route_not_matched(self, model):
        """
        .is_highlited should return False if route is not matched
        """
        assert model.is_highlited() is False

    def test_is_highlited_route_matched(self, model, widget):
        """
        .is_highlited should return False if route is matched but room_id do not
        match
        """
        model.route = widget.highlighted
        model.route_args[1]['room_id'] = 10
        assert model.is_highlited() is False

    def test_is_highlited_route_and_room_id_matched(
        self,
        model,
        widget,
        matchdict
    ):
        """
        .is_highlited should return True if route and room_id match
        """
        matchdict['room_id'] = '10'
        model.route = widget.highlighted
        model.route_args[1]['room_id'] = 10
        assert model.is_highlited() is True
