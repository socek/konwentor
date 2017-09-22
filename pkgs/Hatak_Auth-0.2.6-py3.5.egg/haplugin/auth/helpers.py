from jinja2.exceptions import TemplateNotFound

from haplugin.formskit.helpers import FormWidget


class LoginFormWidget(FormWidget):

    prefix = 'haplugin.auth:templates/forms'

    def render_for(self, name, data, prefix=None):
        self.generate_data()
        self.data.update(data)
        prefix = prefix or self.prefix
        try:
            return self.render(self.get_template(name, prefix))
        except TemplateNotFound:
            return self.render(self.get_template(name, super().prefix))
