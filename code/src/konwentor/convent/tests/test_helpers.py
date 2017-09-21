from pytest import fixture, yield_fixture
from mock import MagicMock, patch

from hatak.testing import RequestFixture
from ..helpers import has_access_to_route, ConventWidget


class TestHasAccessToRoute(object):

    def test_success(self):
        """
        has_access_to_route should run decorated method if use has access to
        route.
        """
        method = MagicMock()
        decorator = has_access_to_route('route')
        wrapped = decorator(method)
        obj = MagicMock()
        obj.user.has_access_to_route.return_value = True

        result = wrapped(obj, 'arg', kw='kwarg')

        method.assert_called_once_with(obj, 'arg', kw='kwarg')
        assert result == method.return_value
        obj.user.has_access_to_route.assert_called_once_with('route')

    def test_fail(self):
        """
        has_access_to_route should return '' if use has no access to
        route
        """
        method = MagicMock()
        decorator = has_access_to_route('route')
        wrapped = decorator(method)
        obj = MagicMock()
        obj.user.has_access_to_route.return_value = False

        result = wrapped(obj, 'arg', kw='kwarg')

        assert result == ''
        obj.user.has_access_to_route.assert_called_once_with('route')


class TestConventWidget(RequestFixture):

    @fixture
    def convent(self):
        return MagicMock()

    @fixture
    def widget(self, request, convent):
        return ConventWidget(request, convent)

    @yield_fixture
    def render_for(self, widget):
        with patch.object(widget, 'render_for', autospec=True) as mock:
            yield mock

    @yield_fixture
    def ConventDeleteForm(self):
        patcher = patch('konwentor.convent.helpers.ConventDeleteForm')
        with patcher as mock:
            yield mock

    @yield_fixture
    def FormWidget(self):
        patcher = patch('konwentor.convent.helpers.FormWidget')
        with patcher as mock:
            yield mock

    def test_id(self, widget, convent):
        assert widget.id == convent.id

    def test_name(self, widget, convent):
        assert widget.name == convent.name

    def test_state(self, convent, widget):
        convent.state = 'running'
        assert widget.state == 'W trakcie'

    def test_switch(self, convent, widget, render_for):
        result = widget.switch()
        render_for.assert_called_once_with(
            'choose_button.jinja2',
            {
                'url': self.route('convent:choose', obj_id=convent.id)
            }
        )
        assert result == render_for.return_value

    def test_edit(self, widget, convent, render_for):
        result = widget.edit()
        render_for.assert_called_once_with(
            'edit_button.jinja2',
            {
                'url': self.route('convent:edit', obj_id=convent.id)
            }
        )
        assert result == render_for.return_value

    def test_delete(
        self,
        widget,
        convent,
        render_for,
        ConventDeleteForm,
        FormWidget,
        request
    ):
        route = request.route_path
        result = widget.delete()

        render_for.assert_called_once_with(
            'delete_button.jinja2',
            {
                'url': route('convent:delete', obj_id=convent.id),
                'form': FormWidget.return_value,
            }
        )
        form = ConventDeleteForm.return_value

        assert result == render_for.return_value
        FormWidget.assert_called_once_with(self.request, form)
        ConventDeleteForm.assert_called_once_with(self.request)
        assert route('convent:delete', obj_id=convent.id) == form.action

    def test_start_fail(
        self,
        widget,
        convent,
        render_for,
    ):
        convent.is_user_able_to_start.return_value = False
        assert widget.start() == ''
        convent.is_user_able_to_start.assert_called_once_with(
            widget.user)

    def test_start_success(self, widget, convent, render_for):
        convent.is_user_able_to_start.return_value = True

        result = widget.start()

        convent.is_user_able_to_start.assert_called_once_with(
            widget.user)

        render_for.assert_called_once_with(
            'start_button.jinja2',
            {
                'url': self.route('convent:start', obj_id=convent.id),
                'convent': widget.convent,
            }
        )
        assert result == render_for.return_value

    def test_end_fail(self, widget, convent):
        convent.is_user_able_to_end.return_value = False
        assert widget.end() == ''
        convent.is_user_able_to_end.assert_called_once_with(
            widget.user)

    def test_end_success(self, widget, convent, render_for):
        convent.is_user_able_to_end.return_value = True

        result = widget.end()

        convent.is_user_able_to_end.assert_called_once_with(
            widget.user)

        render_for.assert_called_once_with(
            'end_button.jinja2',
            {
                'url': self.route('convent:end', obj_id=convent.id),
            }
        )
        assert result == render_for.return_value

    def test_ended_warning_false(self, widget, convent):
        convent.state = 'running'

        result = widget.ended_warning()

        assert result == ''

    def test_ended_warning_true(self, widget, convent, render_for):
        convent.state = 'ended'

        result = widget.ended_warning()

        render_for.assert_called_once_with(
            'ended_warning.jinja2',
            {}
        )
        assert result == render_for.return_value

    def test_row_class_false(self, widget, convent):
        convent.id = 10
        assert widget.row_class(15) == ''

    def test_row_class_true(self, widget, convent):
        convent.id = 10
        assert widget.row_class(10) == 'danger'
