from haplugin.formskit.helpers import FormWidget as BaseFormWidget


class FormWidget(BaseFormWidget):

    def combobox(self, name, disabled=False, autofocus=False):
        self.request.add_js_link('/js/combobox.js')
        self.request.add_js(
            '''$(document).ready(function() {
                $("#%s").combobox();
                });''' % (self.get_id(name)))
        return self._input('combobox', name, disabled, autofocus)
