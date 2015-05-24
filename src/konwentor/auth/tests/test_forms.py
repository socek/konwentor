from mock import MagicMock, patch, call
from pytest import fixture, yield_fixture

from haplugin.sql.testing import DatabaseFixture

from konwentor.application.testing import FormFixture
from ..forms import IsUniqe, AuthEditForm, AuthAddForm
from ..models import User


class TestIsUniqe(DatabaseFixture):

    @fixture
    def field(self, request):
        field = MagicMock()
        field.form.request = request
        field.form.get_value.return_value = None
        field.name = 'email'
        return field

    @fixture
    def validator(self, field, driver):
        validator = IsUniqe(driver.Auth, User)
        validator.init_field(field)
        return validator

    def test_empty(self, validator):
        """
        IsUniqe should return True when value is empty.
        """
        validator.value = None
        assert validator.validate_value() is True

    def test_not_found(self, validator, fixtures):
        """
        IsUniqe should return True, if email is not found.
        """
        validator.value = 'some@email.com'
        assert validator.validate_value() is True

    def test_found(self, validator, fixtures):
        """
        IsUniqe should return False, if email is found.
        """
        validator.value = fixtures['User']['first'].email
        assert validator.validate_value() is False

    def test_for_model_with_id(self, validator, fixtures, field):
        """
        IsUniqe should return True, if email is found only for object assigned
        to this form.
        """
        field.form.get_value.return_value = fixtures['User']['first'].id
        validator.value = fixtures['User']['first'].email
        assert validator.validate_value() is True

    def test_no_id_field(self, validator, fixtures, field):
        '''
        IsUniqe should use id=None when no id field in form.
        '''
        field.form.get_value.side_effect = KeyError
        validator.value = fixtures['User']['first'].email
        assert validator.validate_value() is False


class TestAuthEditForm(FormFixture):

    def _get_form_class(self):
        return AuthEditForm

    @yield_fixture
    def set_value(self, form):
        patcher = patch.object(form, 'set_value')
        with patcher as mock:
            yield mock

    @yield_fixture
    def get_values(self, form):
        patcher = patch.object(form, 'get_values')
        with patcher as mock:
            yield mock

    def test_fill(self, form, set_value):
        user = MagicMock()
        perm = MagicMock()
        perm.name = 'myname'
        perm.group = 'mygroup'
        user.permissions = [perm]

        form.fill(user)

        set_value.assert_has_calls([
            call('id', user.id),
            call('name', user.name),
            call('email', user.email),
            call('permission', 'mygroup:myname', 0)
        ])

    def test_get_permissions_from_forms(self, form, get_values):
        """
        _get_permissions_from_forms should split all permission form values
        into (group, name) list.
        """
        get_values.return_value = ['mygroup:myname', '']

        assert list(form._get_permissions_from_forms()) == [
            ['mygroup', 'myname']
        ]

    def test_on_success(self, form, mdriver):
        form.parse_dict({
            'name': 'myname',
            'email': 'myemail',
            'permission': ['mygroup1:myname1', 'mygroup2:myname2']
        })
        form.model = MagicMock()
        form.model.permissions = [
            MagicMock(),
            MagicMock(),
        ]
        form.model.permissions[0].group = 'mygroup1'
        form.model.permissions[0].name = 'myname1'
        form.model.permissions[1].group = 'mygroup3'
        form.model.permissions[1].name = 'myname3'

        form.on_success()

        form.model.name == 'myname'
        form.model.email == 'email'

        mdriver.Auth.add_permission.assert_has_calls([
            call(form.model, 'mygroup1', 'myname1'),
            call(form.model, 'mygroup2', 'myname2'),
        ])

        mdriver.Auth.remove_permission.assert_called_once_with(
            form.model,
            'mygroup3',
            'myname3',
        )


class TestAuthAddForm(FormFixture):

    def _get_form_class(self):
        return AuthAddForm

    @yield_fixture
    def set_model_values(self, form):
        patcher = patch.object(form, '_set_model_values')
        with patcher as mock:
            yield mock

    def test_on_success(self, form, mdriver, set_model_values):
        '''
        .on_success should create new User object.
        '''
        form.on_success()

        mdriver.Auth.create.assert_called_once_with()
        set_model_values.assert_called_once_with()
