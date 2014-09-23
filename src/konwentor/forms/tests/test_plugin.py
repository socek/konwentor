from mock import create_autospec, MagicMock

from hatak.controller import Controller
from hatak.plugins.toster.cases import TestCase

from konwentor.forms.helpers import FormWidget
from konwentor.forms.plugin import FormControllerPlugin


class FormControllerPluginTest(TestCase):
    prefix_from = FormControllerPlugin

    def setUp(self):
        super().setUp()
        self.request.registry['controller_plugins'] = (
            self.runner.application.controller_plugins)
        self.root = MagicMock()
        self.controller = create_autospec(Controller(self.root, self.request))
        self.ctrlplugin = self.prefix_from(self.controller)

    def test_add_controller_methods(self):
        """add_controller_methods should add add_form to controller"""
        self.ctrlplugin.add_controller_methods()

        self.assertEqual(
            self.ctrlplugin.add_form,
            self.controller.add_form)

    def test_add_form(self):
        """add_form should add form wrapped with FormWidget"""
        formcls = MagicMock()

        result = self.ctrlplugin.add_form(formcls, 'name', 'arg', kwarg='one')

        formcls.assert_called_once_with(
            self.ctrlplugin.request, 'arg', kwarg='one')
        form = formcls.return_value
        self.controller.add_helper.assert_called_once_with(
            'name', FormWidget, form)
        self.assertEqual(form, result)
