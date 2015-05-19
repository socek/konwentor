from haplugin.formskit.helpers import FormWidget as BaseFormWidget


class FormWidget(BaseFormWidget):
    konwentor_prefix = 'konwentor.forms:templates'

    def combobox(self, name, disabled=False, autofocus=False):
        self.request.add_js_link('/js/combobox.js')
        self.request.add_js(
            '''$(document).ready(function() {
                $("#%s").combobox();
                });''' % (self.get_id(name)))
        return self._input('combobox', name, disabled, autofocus)

    def text_with_add(
        self,
        name,
        disabled=False,
        autofocus=False,
        button_label='Add',
    ):
        self.request.add_js_link('/js/add_button.js')
        self.request.add_js('''
            $(document).ready(function() {
                $(".addroom").addroom();
            });
        ''')
        return self._input(
            'text_with_add',
            name,
            disabled,
            autofocus,
            prefix=self.konwentor_prefix,
            button_label=button_label,
        )
