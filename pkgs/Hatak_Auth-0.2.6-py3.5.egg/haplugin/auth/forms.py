from formskit.formvalidators import FormValidator
from formskit.validators import NotEmpty

from haplugin.formskit import PostForm
from hatak.unpackrequest import unpack


class EmailMustExists(FormValidator):

    message = "EmailMustExists"

    def validate(self):
        unpack(self, self.form.request)
        email = self.form.get_value('email')
        self.form._user = self.driver.Auth.get_by_email(email)
        return self.form._user is not None


class PasswordMustMatch(FormValidator):

    message = "PasswordMustMatch"

    def validate(self):
        data = self.form.get_data_dict(True)
        return self.form._user.validate_password(data['password'])


class LoginForm(PostForm):

    def create_form(self):
        self.add_field('email', label='E-mail', validators=[NotEmpty()])
        self.add_field('password', label='Hasło', validators=[NotEmpty()])

        self.add_form_validator(EmailMustExists())
        self.add_form_validator(PasswordMustMatch())

    def on_success(self):
        self.session['user_id'] = self._user.id
