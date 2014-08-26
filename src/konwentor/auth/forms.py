from formskit import Field
from formskit.formvalidators import FormValidator

from konwentor.forms.validators import NotEmpty
from konwentor.forms.models import PostForm

from .models import User


class EmailMustExists(FormValidator):

    message = "Email i/lub hasło są nieprawidłowe."

    def validate(self):
        db = self.form.db

        email = self.form.get_value('email')
        user = db.query(User).filter_by(email=email).first()
        if user is None:
            return False
        else:
            self.form.user = user
            return True


class LoginForm(PostForm):

    def createForm(self):
        self.addField(
            Field('email', label='E-mail', validators=[NotEmpty()]))
        self.addField(
            Field('password', label='Hasło', validators=[NotEmpty()]))

        self.addFormValidator(EmailMustExists())

    def overalValidation(self, data):
        self.user = self.db.query(User).filter_by(email=data['email'][0]).one()
        if self.user.validate_password(data['password'][0]):
            return True
        else:
            self.message = "Email i/lub hasło są nieprawidłowe."
            return False

    def submit(self, data):
        self.session['user_id'] = self.user.id
