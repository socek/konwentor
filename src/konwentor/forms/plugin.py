from hatak.plugins.plugin import Plugin
from hatak.controller import ControllerPlugin

from konwentor.forms.helpers import FormWidget


class FormPlugin(Plugin):

    def add_controller_plugins(self, plugins):
        plugins.append(FormControllerPlugin)


class FormControllerPlugin(ControllerPlugin):

    def before_filter(self):
        self.controller.add_form = self.add_form

    def add_controller_methods(self):
        self.add_method('add_form')

    def add_form(self, formcls, name='form', *args, **kwargs):
        form = formcls(self.request, *args, **kwargs)
        self.controller.add_helper(name, FormWidget, form)
        return form
