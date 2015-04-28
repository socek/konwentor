from sqlalchemy.orm.exc import NoResultFound
from pytest import fixture, yield_fixture
from mock import patch, MagicMock

from hatak.testing import RequestFixture

from ..helpers import TopMenuWidget, OnConventMenuObject


class TestTopMenuWidget(RequestFixture):

    @fixture
    def widget(self, request):
        self.highlighted = 'highlited'
        widget = TopMenuWidget(request, self.highlighted)
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


class TestOnConventMenuObject(object):

    @fixture
    def widget(self):
        return MagicMock()

    @fixture
    def obj(self, widget):
        return OnConventMenuObject(widget)

    @fixture
    def session(self, obj):
        obj.session = {}
        return obj.session

    @yield_fixture
    def add_child(self):
        patcher = patch.object(OnConventMenuObject, 'add_child')
        with patcher as mock:
            yield mock

    def test_is_avalible(self, obj, session):
        """
        .is_avalible should return True if convent_id is set in the session
        """
        assert obj.is_avalible() is False

        session['convent_id'] = 'something'
        assert obj.is_avalible() is True

    def test_creating_when_no_convent_set(self, widget, add_child):
        """
        Creating OnConventMenuObject should not add any childs when no
        convent found.
        """
        driver = widget.request.driver.Convent
        driver.get_convent_from_session.side_effect = NoResultFound

        OnConventMenuObject(widget)

        assert add_child.called is False

    def test_creating(self, widget, add_child):
        """
        Creating OnConventMenuObject should add child for every room at convent
        """
        convent = MagicMock()
        room = MagicMock()
        room.name = 'room name'
        convent.rooms = [room]
        driver = widget.request.driver.Convent
        driver.get_convent_from_session.return_value = convent

        OnConventMenuObject(widget)

        add_child.assert_called_once_with('room name', 'gamecopy:add', 'magic')
