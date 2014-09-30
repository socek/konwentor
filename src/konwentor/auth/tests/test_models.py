from mock import MagicMock
from hatak.controller import Controller
from haplugin.toster import ModelTestCase
from mock import create_autospec

from konwentor.auth.models import User, NotLoggedUser


class UserTestCase(ModelTestCase):
    prefix_from = User

    def test_password(self):
        """Setted password should be validated. Wrong one should not."""
        self.model.set_password('god')

        self.assertEqual(True, self.model.validate_password('god'))
        self.assertEqual(False, self.model.validate_password('god2'))

    def test_is_logged(self):
        """User should always be logged. Only FakeUser should not be logged."""
        self.assertEqual(True, self.model.is_logged())

    def test_add_permission(self):
        """add_permission should get or create Permission and assing it to User
        """
        self.add_mock('Permission')

        self.model.add_permission(self.db, 'first', 'second')

        self.mocks['Permission'].get_or_create.assert_called_once_with(
            self.db,
            group='first',
            name='second')

        self.assertEqual(
            [self.mocks['Permission'].get_or_create.return_value],
            self.model.permissions)

    def test_has_permission_success(self):
        """has_permission should return True if permission is in user
        permissions"""
        permission = MagicMock()
        permission.name = 'name'
        permission.group = 'group'
        self.model.permissions.append(permission)
        self.assertEqual(True, self.model.has_permission('group', 'name'))

    def test_has_permission_fail(self):
        """has_permission should return False if permission is not in user
        permissions"""
        self.assertEqual(False, self.model.has_permission('group', 'name'))

        permission = MagicMock()
        self.model.permissions.append(permission)
        permission.name = 'bad name'
        permission.group = 'group'
        self.assertEqual(False, self.model.has_permission('group', 'name'))

    def test_has_access_to_route(self):
        """has_access_to_route should find controller and use
        has_access_to_controller"""
        self.add_mock_object(self.model, 'has_access_to_controller')
        self.registry['route'] = MagicMock()
        self.registry['route'].routes = {
            'myroute': 'ctrl',
        }
        self.model.registry = self.registry

        result = self.model.has_access_to_route('myroute')

        self.assertEqual(
            self.mocks['has_access_to_controller'].return_value, result)
        self.mocks['has_access_to_controller'].assert_called_once_with('ctrl')

    def test_has_access_to_controller_success(self):
        """has_access_to_controller should get permissions from ctrl, and
        return True if user has all permissions"""
        ctrl = MagicMock()
        ctrl.permissions = [('base', 'view')]
        self.add_mock_object(self.model, 'has_permission')
        self.mocks['has_permission'].return_value = True

        self.assertEqual(True, self.model.has_access_to_controller(ctrl))

        self.mocks['has_permission'].assert_called_once_with('base', 'view')

    def test_has_access_to_controller_fail(self):
        """has_access_to_controller should get permissions from ctrl, and
        return False if user has not one of that permissions"""
        ctrl = MagicMock()
        ctrl.permissions = [('base', 'view')]
        self.add_mock_object(self.model, 'has_permission')
        self.mocks['has_permission'].return_value = False

        self.assertEqual(False, self.model.has_access_to_controller(ctrl))

        self.mocks['has_permission'].assert_called_once_with('base', 'view')


class NotLoggedUserTestCase(ModelTestCase):
    prefix_from = NotLoggedUser

    def test_has_permission(self):
        """FakeUser should not have any permissions."""
        self.assertEqual(False, self.model.has_permission('base', 'view'))

    def test_add_permission(self):
        """FakeUser can not add permission."""
        self.assertRaises(
            NotImplementedError, self.model.add_permission, ('base', 'view'))

    def test_set_password(self):
        """FakeUser can not change his password."""
        self.assertRaises(
            NotImplementedError, self.model.set_password, ('password',))

    def test_validate_password(self):
        """FakeUser can not check his password."""
        self.assertRaises(
            NotImplementedError, self.model.validate_password, ('password',))

    def test_is_logged(self):
        """FakeUser is not and can not be logged."""
        self.assertEqual(False, self.model.is_logged())

    def test_has_access_to_controller(self):
        """FakeUser has access only to controllers without permissions."""
        ctrl = create_autospec(Controller)
        self.assertEqual(True, self.model.has_access_to_controller(ctrl))

        ctrl.permissions = [1]
        self.assertEqual(False, self.model.has_access_to_controller(ctrl))
