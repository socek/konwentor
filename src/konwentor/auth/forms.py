from formskit.validators import NotEmpty, FieldValidator, IsDigit
from formskit.formvalidators import MustMatch

from konwentor.convent.forms import IdExists
from haplugin.formskit import PostForm
from .models import User


class IsUniqe(FieldValidator):

    def __init__(self, driver, cls):
        super().__init__()
        self.cls = cls

    @property
    def request(self):
        return self.field.form.request

    def validate_value(self):
        driver = self.request.driver.Auth
        field_name = self.field.name
        if self.value is None:
            return True
        else:
            kwargs = {
                field_name: self.value,
            }
            try:
                model_id = self.field.form.get_value('id', default=None)
            except KeyError:
                model_id = None
            items = (
                driver.find_by(**kwargs)
                .filter(self.cls.id != model_id)
                .count()
            )
            return items == 0


class AuthAddForm(PostForm):

    def create_form(self):
        super().create_form()
        self.add_field('name', label='Imię', validators=[NotEmpty()])
        self.add_field(
            'email',
            label='Email',
            validators=[
                NotEmpty(),
                IsUniqe(self.driver.Auth, User)
            ]
        )
        self._create_password_fields()
        self.add_field('permission', label='Prawa')

    def _create_password_fields(self):
        self.add_field(
            'password1',
            label='Hasło',
            validators=[
                NotEmpty(),
            ]
        )

        self.add_field(
            'password2',
            label='Hasło (powtórzone)',
            validators=[
                NotEmpty(),
            ]
        )
        self.add_form_validator(MustMatch(['password1', 'password2']))

    def _add_missing_permissions(self, permissions):
        for group, name in permissions:
            self.driver.Auth.add_permission(self.model, group, name)

    def _get_permissions_from_forms(self):
        for permission in self.get_values('permission'):
            if permission:
                yield permission.split(':')

    def _delete_removed_permissions(self, permissions):
        for permission in self._get_permissions_to_delete(permissions):
            self.driver.Auth.remove_permission(
                self.model,
                permission.group,
                permission.name
            )

    def _get_permissions_to_delete(self, permissions):
        for permission in self.model.permissions:
            permission_name = [permission.group, permission.name]
            if permission_name not in permissions:
                yield permission

    def on_success(self):
        self._create_model()
        self._set_model_values()

    def _create_model(self):
        self.model = self.driver.Auth.create()

    def _set_model_values(self):
        self.model.name = self.get_value('name')
        self.model.email = self.get_value('email')
        self._update_password()
        permissions = list(self._get_permissions_from_forms())
        self._add_missing_permissions(permissions)
        self._delete_removed_permissions(permissions)

    def _update_password(self):
        password = self.get_value('password1', default=None)
        if password:
            self.model.set_password(password)


class AuthEditForm(AuthAddForm):

    def create_form(self):
        super().create_form()
        self.add_field('id', validators=[NotEmpty(), IsDigit()])

        self.add_form_validator(IdExists('Auth'))

    def _create_password_fields(self):
        self.add_field(
            'password1',
            label='Hasło',
            validators=[
            ]
        )

        self.add_field(
            'password2',
            label='Hasło (powtórzone)',
            validators=[
            ]
        )
        self.add_form_validator(MustMatch(['password1', 'password2']))

    def _create_model(self):
        """
        model is created by .fill
        """

    def fill(self, user):
        self.set_value('id', user.id)
        self.set_value('name', user.name)
        self.set_value('email', user.email)
        for index, permission in enumerate(user.permissions):
            name = '%s:%s' % (permission.group, permission.name)
            self.set_value('permission', name, index)

        self.model = user
