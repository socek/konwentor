from mock import patch, MagicMock
from pytest import yield_fixture, fixture

from hatak.testing import RequestFixture


class FormFixture(RequestFixture):

    def _get_form_class(self):
        pass

    @yield_fixture
    def CsrfMustMatch(self):
        with patch('haplugin.formskit.models.CsrfMustMatch') as mock:
            yield mock

    @fixture
    def form(self, request):
        cls = self._get_form_class()
        form = cls(request)
        defaults = {
            form.form_name_value: [form.get_name(), ]
        }
        request.POST.dict_of_lists.return_value = defaults
        return form

    @fixture
    def postdata(self, request, form):
        return request.POST.dict_of_lists.return_value


class FormWidgetFixture(RequestFixture):

    def _get_widget_class(self):
        pass

    @fixture
    def form(self):
        return MagicMock()

    @fixture
    def widget(self, request, form):
        return self._get_widget_class()(request, form)

    @yield_fixture
    def render_for(self, widget):
        with patch.object(widget, 'render_for', autospec=True) as mock:
            yield mock

    def _input_test(
        self,
        render_for,
        widget,
        form,
        name,
        method_name=None,
        external=None,
        **kwargs
    ):
        method_name = method_name or name
        input_name = 'myname'
        external = external or {}

        method = getattr(widget, method_name)
        result = method(input_name, True, False)
        field = form.fields[name]

        data = {
            'name': field.get_name(),
            'value': form.get_value.return_value,
            'values': form.get_values.return_value,
            'field': field,
            'id': '%s_myname' % (form.get_name()),
            'label': field.label,
            'error': field.error,
            'messages': (
                form.fields.__getitem__.return_value
                .get_error_messages.return_value
            ),
            'value_messages': (
                form.fields.__getitem__.return_value
                .get_value_errors.return_value
            ),
            'disabled': True,
            'autofocus': False,
        }
        data.update(external)

        self.assert_render_for(
            result,
            render_for,
            name + '.jinja2',
            data,
            **kwargs
        )

    def assert_render_for(self, result, render_for, *args, **kwargs):
        assert result == render_for.return_value
        render_for.assert_called_once_with(*args, **kwargs)


class FormControllerFixture(object):

    @yield_fixture
    def add_form(self, controller):
        with patch.object(controller, 'add_form', autospec=True) as mock:
            yield mock

    @fixture
    def form(self, add_form):
        return add_form.return_value
