from mock import MagicMock
from hatak.tests.cases import TestCase

from ..helpers import has_access_to_route, ConventWidget


class HasAccessToRouteTests(TestCase):
    prefix_from = has_access_to_route

    def test_success(self):
        """has_access_to_route should run decorated method if use has access to
        route"""
        method = MagicMock()
        decorator = has_access_to_route('route')
        wrapped = decorator(method)
        obj = MagicMock()
        obj.user.has_access_to_route.return_value = True

        result = wrapped(obj, 'arg', kw='kwarg')

        method.assert_called_once_with(obj, 'arg', kw='kwarg')
        self.assertEqual(
            method.return_value,
            result
        )
        obj.user.has_access_to_route.assert_called_once_with('route')

    def test_fail(self):
        """has_access_to_route should return '' if use has no access to
        route"""
        method = MagicMock()
        decorator = has_access_to_route('route')
        wrapped = decorator(method)
        obj = MagicMock()
        obj.user.has_access_to_route.return_value = False

        result = wrapped(obj, 'arg', kw='kwarg')

        self.assertEqual(
            '',
            result
        )
        obj.user.has_access_to_route.assert_called_once_with('route')


class ConventWidgetTests(TestCase):
    prefix_from = ConventWidget

    def setUp(self):
        super().setUp()
        self.convent = MagicMock()
        self.widget = ConventWidget(self.request, self.convent)
        self.add_mock_object(self.widget, 'render_for')

    def test_id(self):
        self.assertEqual(self.convent.id, self.widget.id)

    def test_name(self):
        self.assertEqual(self.convent.name, self.widget.name)

    def test_state(self):
        self.convent.state = 'running'
        self.assertEqual('W trakcie', self.widget.state)

    def test_switch(self):
        result = self.widget.switch()
        self.mocks['render_for'].assert_called_once_with(
            'choose_button',
            {
                'url': self.route('convent:choose', obj_id=self.convent.id)
            }
        )
        self.assertEqual(
            self.mocks['render_for'].return_value,
            result)

    def test_delete(self):
        self.add_mock('ConventDeleteForm')
        self.add_mock('FormWidget')

        result = self.widget.delete()

        self.mocks['render_for'].assert_called_once_with(
            'delete_button',
            {
                'url': self.route('convent:delete', obj_id=self.convent.id),
                'form': self.mocks['FormWidget'].return_value,
            }
        )
        form = self.mocks['ConventDeleteForm'].return_value
        self.assertEqual(
            self.mocks['render_for'].return_value,
            result)
        self.mocks['FormWidget'].assert_called_once_with(self.request, form)
        self.mocks['ConventDeleteForm'].assert_called_once_with(self.request)
        self.assertEqual(
            self.route('convent:delete', obj_id=self.convent.id),
            form.action)

    def test_start_fail(self):
        self.convent.is_user_able_to_start.return_value = False
        self.assertEqual('', self.widget.start())
        self.convent.is_user_able_to_start.assert_called_once_with(
            self.widget.user)

    def test_start_success(self):
        self.convent.is_user_able_to_start.return_value = True

        result = self.widget.start()

        self.convent.is_user_able_to_start.assert_called_once_with(
            self.widget.user)

        self.mocks['render_for'].assert_called_once_with(
            'start_button',
            {
                'url': self.route('convent:start', obj_id=self.convent.id),
                'convent': self.widget.convent,
            }
        )
        self.assertEqual(
            self.mocks['render_for'].return_value,
            result)

    def test_end_fail(self):
        self.convent.is_user_able_to_end.return_value = False
        self.assertEqual('', self.widget.end())
        self.convent.is_user_able_to_end.assert_called_once_with(
            self.widget.user)

    def test_end_success(self):
        self.convent.is_user_able_to_end.return_value = True

        result = self.widget.end()

        self.convent.is_user_able_to_end.assert_called_once_with(
            self.widget.user)

        self.mocks['render_for'].assert_called_once_with(
            'end_button',
            {
                'url': self.route('convent:end', obj_id=self.convent.id),
            }
        )
        self.assertEqual(
            self.mocks['render_for'].return_value,
            result)

    def test_ended_warning_false(self):
        self.convent.state = 'running'

        result = self.widget.ended_warning()

        self.assertEqual('', result)

    def test_ended_warning_true(self):
        self.convent.state = 'ended'

        result = self.widget.ended_warning()

        self.mocks['render_for'].assert_called_once_with(
            'ended_warning',
            {}
        )
        self.assertEqual(
            self.mocks['render_for'].return_value,
            result)

    def test_row_class_false(self):
        self.convent.id = 10
        self.assertEqual('', self.widget.row_class(15))

    def test_row_class_true(self):
        self.convent.id = 10
        self.assertEqual('danger', self.widget.row_class(10))
