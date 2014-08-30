from jinja2.exceptions import TemplateNotFound

from konwentor.forms.helpers import FormWidget


class LoginFormWidget(FormWidget):

    prefix = 'konwentor.auth:templates/forms'

    def render_for(self, name, data):
        self.generate_data()
        self.data.update(data)
        try:
            return self.render(self.get_template(name, self.prefix))
        except TemplateNotFound:
            return self.render(self.get_template(name, super().prefix))
