from pytest import fixture, yield_fixture
from mock import MagicMock, patch

from hatak.testing import RequestFixture
from ..helpers import LinkWidget, render_when_has_access


class TestRenderWhenhasAccess(object):

    def test_render_when_has_access_when_has_access(self):
        """
        render_when_has_access decorator should return result of method when
        user has access to route
        """
        method = MagicMock()
        mself = MagicMock()
        mself.user.has_access_to_route.return_value = True

        wrapped = render_when_has_access(method)
        result = wrapped(mself, 'name', 'myroute', 'arg', kw='arg')
        assert result == method.return_value
        method.assert_called_once_with(
            mself, 'name', 'myroute', 'arg', kw='arg')

    def test_render_when_has_access_when_has_not_access(self):
        """
        render_when_has_access decorator should return empty string when user
        has no access to route
        """
        method = MagicMock()
        mself = MagicMock()
        mself.user.has_access_to_route.return_value = False

        wrapped = render_when_has_access(method)
        result = wrapped(mself, 'name', 'myroute', 'arg', kw='arg')
        assert result == ''
        assert not method.called


class TestLinkWidget(RequestFixture):

    @fixture
    def widget(self, request):
        return LinkWidget(request)

    @yield_fixture
    def render_for(self, widget):
        patcher = patch.object(widget, 'render_for')
        with patcher as mock:
            yield mock

    @fixture
    def route(self, request):
        return request.route_path

    def test_button(self, widget, render_for, route):
        """
        button should be proper rendered
        """
        assert widget.button('name', 'myroute') == render_for.return_value
        render_for.assert_called_once_with('button.haml', {
            'url': route.return_value,
            'name': 'name',
        })

    def test_link(self, widget, render_for, route):
        """
        link should be proper rendered
        """
        assert widget.link('name', 'myroute') == render_for.return_value
        render_for.assert_called_once_with('link.haml', {
            'url': route.return_value,
            'name': 'name',
        })
