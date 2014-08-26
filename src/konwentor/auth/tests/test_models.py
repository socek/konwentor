from hatak.controller import Controller
from hatak.tests.cases import ModelTestCase
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
