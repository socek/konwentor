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

    def test_is_avalible(self, obj, session):
        """
        .is_avalible should return True if convent_id is set in the session
        """
        assert obj.is_avalible() is False

        session['convent_id'] = 'something'
        assert obj.is_avalible() is True
