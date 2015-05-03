from pytest import fixture, yield_fixture
from mock import MagicMock, patch

from hatak.testing import RequestFixture

from ..models import MenuObject


class TestMenuObject(RequestFixture):

    @fixture
    def widget(self, request):
        widget = MagicMock()
        widget.request = request
        return widget

    @fixture
    def model(self, widget):
        self.name = 'name'
        self.rotue = 'route'
        self.icon = 'icon'
        return MenuObject(
            widget,
            self.name,
            self.route,
            self.icon,
            'arg',
            kw='arg'
        )

    @yield_fixture
    def MenuObject(self):
        with patch('konwentor.menu.models.MenuObject') as mock:
            yield mock

    def test_init(self, widget, model, request):
        assert model.widget == widget
        assert model.request == request
        assert model.session == request.session
        assert model.highlighted == widget.highlighted
        assert model.name == self.name
        assert model.route == self.route
        assert model.route_args == (('arg',), {'kw': 'arg'})
        assert model.icon == self.icon
        assert model.childs == []

    def test_get_url_success(self, model, request):
        """get_url should return route path if specyfied"""
        assert model.get_url() == request.route_path.return_value

        self.request.route_path.assert_called_once_with(
            model.route,
            'arg',
            kw='arg'
        )

    def test_get_url_fail(self, model):
        """get_url should return '#' if route not specyfied"""
        model.route = None

        assert model.get_url() == '#'

    def test_is_highlited(self, model):
        """
        is_highlited should return True if self.route is poting where
        Menu.highlighted
        """
        model.highlighted = 'route'
        model.route = 'route'
        assert model.is_highlited() is True

    def test_get_icon(self, model):
        """get_icon should return class name describeing icon"""
        assert model.get_icon() == 'fa-icon'

    def test_is_visible_success(self, model, request):
        """
        is_visible should return has_access_to_route when the route is set
        """
        result = model.is_visible()
        assert result == self.request.user.has_access_to_route.return_value
        request.user.has_access_to_route.assert_called_once_with(model.route)

    def test_is_visible_fail(self, model):
        """is_visible should return True if no route specyfied"""
        model.route = None
        assert model.is_visible() is True

    def test_add_child(self, model, MenuObject):
        """Should append MenuObject to MenuObject.childs."""
        model.add_child('something', kw='arg')

        assert model.childs == [MenuObject.return_value]
        MenuObject.assert_called_once_with(model.widget, 'something', kw='arg')

    def test_get_css_class_when_not_avalible(self, model):
        """
        .get_css_class should return disabled class when MenuObject is disabled
        """
        def is_avalible():
            return False
        model.is_avalible = is_avalible

        assert model.get_css_class() == 'class="disabled"'

    def test_get_css_class_when_highlited(self, model):
        """
        .get_css_class should return active class when is highlighted
        """
        def is_highlited():
            return True
        model.is_highlited = is_highlited

        assert model.get_css_class() == 'class="active"'

    def test_get_css_class(self, model):
        """
        .get_css_class should return empty string when is not disabled and not
        highlighted
        """
        assert model.get_css_class() == ''
