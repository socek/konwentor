from jinja2.exceptions import TemplateNotFound

from konwentor.application.helpers import FormWidget


class LoginFormWidget(FormWidget):

    prefix = 'auth/forms'

    def render_for(self, name, data):
        self.generate_data()
        self.data.update(data)
        try:
            return self.render(self.get_template(name))
        except TemplateNotFound:
            return self.render(self.get_template(name, super().prefix))
