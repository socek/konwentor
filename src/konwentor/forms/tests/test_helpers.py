from mock import MagicMock

from haplugin.formskit.tests.test_helpers import FormWidgetTestCase as Base

from ..helpers import FormWidget


class FormWidgetTestCase(Base):
    prefix_from = FormWidget

    def setUp(self):
        super().setUp()
        self.form = MagicMock()

        self.widget = FormWidget(self.request, self.form)
        self.add_mock_object(self.widget, 'render_for', autospec=True)

    def test_combobox(self):
        self._input_test('combobox')

        self.request.add_js_link.assert_called_once_with('/js/combobox.js')
        self.request.add_js.assert_called_once_with(
            '''$(document).ready(function() {
                $("#%s").combobox();
                });''' % (self.widget.get_id('myname')))
