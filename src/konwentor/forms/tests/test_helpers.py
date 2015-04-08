from haplugin.formskit.testing import FormWidgetFixture

from ..helpers import FormWidget


class TestFormWidget(FormWidgetFixture):

    def _get_widget_class(self):
        return FormWidget

    def test_combobox(self, request, widget, form, render_for):
        self._input_test(render_for, widget, form, 'combobox')

        request.add_js_link.assert_called_once_with('/js/combobox.js')
        request.add_js.assert_called_once_with(
            '''$(document).ready(function() {
                $("#%s").combobox();
                });''' % (widget.get_id('myname')))
