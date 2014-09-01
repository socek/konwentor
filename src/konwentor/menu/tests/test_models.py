from mock import MagicMock
from hatak.tests.cases import TestCase

from ..models import MenuObject


class MenuObjectTests(TestCase):
    prefix_from = MenuObject

    def setUp(self):
        super().setUp()
        self.widget = MagicMock()
        self.widget.request = self.request
        self.name = 'name'
        self.rotue = 'route'
        self.icon = 'icon'
        self.model = MenuObject(self.widget, self.name, self.route, self.icon)

    def test_init(self):
        self.assertEqual(self.widget, self.model.widget)
        self.assertEqual(self.request, self.model.request)
        self.assertEqual(self.session, self.model.session)
        self.assertEqual(self.widget.highlighted, self.model.highlighted)
        self.assertEqual(self.name, self.model.name)
        self.assertEqual(self.route, self.model.route)
        self.assertEqual(self.icon, self.model.icon)
        self.assertEqual([], self.model.childs)

    def test_get_url_success(self):
        """get_url should return route path if specyfied"""
        self.assertEqual(
            self.request.route_path.return_value,
            self.model.get_url())

        self.request.route_path.assert_called_once_with(self.model.route)

    def test_get_url_fail(self):
        """get_url should return '#' if route not specyfied"""
        self.model.route = None

        self.assertEqual('#', self.model.get_url())

    def test_is_highlited(self):
        """is_highlited should return True if self.route is poting where
        Menu.highlighted"""
        self.model.highlighted = 'route'
        self.model.route = 'route'
        self.assertEqual(True, self.model.is_highlited())

    def test_get_icon(self):
        """get_icon should return class name describeing icon"""
        self.assertEqual('fa-icon', self.model.get_icon())

    def test_is_visible_success(self):
        """is_visible should return has_access_to_route when the route is set
        """
        result = self.model.is_visible()
        self.assertEqual(
            self.request.user.has_access_to_route.return_value,
            result)
        self.request.user.has_access_to_route.assert_called_once_with(
            self.model.route)

    def test_is_visible_fail(self):
        """is_visible should return True if no route specyfied"""
        self.model.route = None
        self.assertEqual(True, self.model.is_visible())

    def test_add_child(self):
        """Should append MenuObject to MenuObject.childs."""
        self.add_mock('MenuObject')
        self.model.add_child('something', kw='arg')

        self.assertEqual(
            [self.mocks['MenuObject'].return_value], self.model.childs)
        self.mocks['MenuObject'].assert_called_once_with(
            self.model.widget, 'something', kw='arg')
