from haplugin.formskit.testing import FormWidgetFixture

from ..helpers import FormWidget


class TestFormWidget(FormWidgetFixture):

    def _get_widget_class(self):
        return FormWidget

    def test_combobox(self, request, widget, form, render_for):
        self._input_test(
            render_for,
            widget, form,
            'combobox',
            prefix=None,
        )

        request.add_js_link.assert_called_once_with('/js/combobox.js')
        request.add_js.assert_called_once_with(
            '''$(document).ready(function() {
                $("#%s").combobox();
                });''' % (widget.get_id('myname')))

    def test_text_with_add(self, request, widget, form, render_for):
        self._input_test(
            render_for,
            widget,
            form,
            'text_with_add',
            prefix=FormWidget.konwentor_prefix,
            external={'button_label': 'Add'},
        )

        request.add_js_link.assert_called_once_with('/js/add_button.js')
        request.add_js.assert_called_once_with('''
            $(document).ready(function() {
                $(".addroom").addroom();
            });
        ''')

    def test_text_with_add_from_list(self, request, widget, form, render_for):
        self._input_test(
            render_for,
            widget,
            form,
            'text_with_add_from_list',
            prefix=FormWidget.konwentor_prefix,
            external={'button_label': 'Add', 'elements': []},
        )

        request.add_js_link.assert_called_once_with('/js/add_button.js')
        request.add_js.assert_called_once_with('''
            $(document).ready(function() {
                $(".add_from_list").add_from_list();
                $(".remove_button").remove_button();
            });
        ''')
