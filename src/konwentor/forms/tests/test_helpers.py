from mock import MagicMock

from hatak.tests.cases import TestCase

from ..helpers import FormWidget


class FormWidgetTestCase(TestCase):
    prefix_from = FormWidget

    def setUp(self):
        super().setUp()
        self.form = MagicMock()

        self.widget = FormWidget(self.request, self.form)
        self.add_mock_object(self.widget, 'render_for', autospec=True)

    def assert_render_for(self, result, *args, **kwargs):
        self.assertEqual(
            self.mocks['render_for'].return_value,
            result)
        self.mocks['render_for'].assert_called_once_with(
            *args, **kwargs)

    def test_begin(self):
        """begin should render <form> tag"""
        result = self.widget.begin('fake_id', 'mystyle')

        self.assert_render_for(
            result,
            'begin',
            {
                'action': self.form.action,
                'id': 'fake_id',
                'name': self.form.name,
                'style': 'mystyle',
            },)

    def test_end(self):
        """end should render </form> tag"""
        result = self.widget.end()

        self.assert_render_for(
            result,
            'end',
            {
            },)

    def test_hidden(self):
        """hidden should render <input type="hidden"> tag"""
        result = self.widget.hidden('myname')

        self.assert_render_for(
            result,
            'hidden',
            {
                'name': 'myname',
                'value': self.form.get_value.return_value
            },)

        self.form.get_value.assert_called_once_with('myname')

    def test_submit(self):
        """submit should render <input type="submit"> tag"""
        result = self.widget.submit('mylabel', 'myclass', 'baseclass')

        self.assert_render_for(
            result,
            'submit',
            {
                'label': 'mylabel',
                'class': 'myclass',
                'base_class': 'baseclass'
            },)

    def test_error(self):
        """error should render form error html"""
        result = self.widget.error()

        self.assert_render_for(
            result,
            'error',
            {
                'error': self.form.error,
                'message': self.form.message,
            },)

    def test_text(self):
        """text should render <input type="text"> tag"""
        self._input_test('text')

    def test_password(self):
        """password should render <input type="password"> tag"""
        self._input_test('password')

    def test_select(self):
        """select should render <input type="select"> tag"""
        self._input_test('select')

    def _input_test(self, name):
        self.form.field_patterns = {
            'myname': 'fake field',
        }

        method = getattr(self.widget, name)
        result = method('myname', True, False)

        self.assert_render_for(
            result,
            name,
            {
                'name': 'myname',
                'id': '%s_myname' % (self.form.name),
                'label': self.form.get_label.return_value,
                'error': self.form.get_error.return_value,
                'message': self.form.get_message.return_value,
                'value': self.form.get_value.return_value,
                'disabled': True,
                'autofocus': False,
                'field': 'fake field',
            },)

        self.form.get_label.assert_called_once_with('myname')
        self.form.get_error.assert_called_once_with('myname')
        self.form.get_message.assert_called_once_with('myname')
        self.form.get_value.assert_called_once_with('myname')
