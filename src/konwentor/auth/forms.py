from formskit import Field
from formskit.formvalidators import FormValidator
from formskit.validators import NotEmpty

from haplugin.formskit import PostForm


class EmailMustExists(FormValidator):

    message = "Email i/lub hasło są nieprawidłowe."

    def validate(self):
        db = self.form.db

        email = self.form.get_value('email')
        user_cls = self.form.request.user_cls
        user = db.query(user_cls).filter_by(email=email).first()
        self.form.user = user
        return not user is None


class LoginForm(PostForm):

    def createForm(self):
        self.addField(
            Field('email', label='E-mail', validators=[NotEmpty()]))
        self.addField(
            Field('password', label='Hasło', validators=[NotEmpty()]))

        self.addFormValidator(EmailMustExists())

    def overalValidation(self, data):
        user_cls = self.request.user_cls
        self.user = (
            self.db.query(user_cls).filter_by(email=data['email'][0]).one()
        )
        if self.user.validate_password(data['password'][0]):
            return True
        else:
            self.message = "Email i/lub hasło są nieprawidłowe."
            return False

    def submit(self, data):
        self.session['user_id'] = self.user.id
