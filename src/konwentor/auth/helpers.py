from jinja2.exceptions import TemplateNotFound

from konwentor.application.helpers import FormHelper


class LoginFormHelper(FormHelper):

    prefix = 'auth/forms'

    def render_for(self, name):
        try:
            return self.render(self.get_template(name))
        except TemplateNotFound:
            return self.render(self.get_template(name, super().prefix))
