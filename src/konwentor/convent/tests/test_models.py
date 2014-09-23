from mock import MagicMock
from hatak.plugins.toster.cases import ModelTestCase

from ..models import Convent


class ConventTests(ModelTestCase):
    prefix_from = Convent

    def test_states(self):
        """Getting and settings states"""
        self.model.state = 'running'
        self.assertEqual('running', self.model.state)

    def test_state_fail(self):
        """Setting invalid state should raise runtimeerror"""
        def method():
            self.model.state = 'invalid'

        self.assertRaises(RuntimeError, method)

    def test_is_user_able_to_start_true(self):
        """is_user_able_to_start should return True if state is not started and
        user has access to convent:start controller."""
        self.model.state = 'not started'
        user = MagicMock()
        user.has_access_to_route.return_value = True

        self.assertEqual(True, self.model.is_user_able_to_start(user))
        user.has_access_to_route.assert_called_once_with('convent:start')

    def test_is_user_able_to_start_when_state_is_running(self):
        """is_user_able_to_start should return False if state is running"""
        self.model.state = 'running'
        user = MagicMock()
        user.has_access_to_route.return_value = True

        self.assertEqual(False, self.model.is_user_able_to_start(user))

    def test_is_user_able_to_start_when_user_has_no_access(self):
        """is_user_able_to_start should return False user has no access to
        convent:start"""
        self.model.state = 'not started'
        user = MagicMock()
        user.has_access_to_route.return_value = False

        self.assertEqual(False, self.model.is_user_able_to_start(user))
        user.has_access_to_route.assert_called_once_with('convent:start')

    def test_is_user_able_to_end_true(self):
        """is_user_able_to_end should return True if state is running and
        user has access to convent:start controller."""
        self.model.state = 'running'
        user = MagicMock()
        user.has_access_to_route.return_value = True

        self.assertEqual(True, self.model.is_user_able_to_end(user))
        user.has_access_to_route.assert_called_once_with('convent:end')

    def test_is_user_able_to_end_when_state_is_ended(self):
        """is_user_able_to_start should return False if state is ended"""
        self.model.state = 'ended'
        user = MagicMock()
        user.has_access_to_route.return_value = True

        self.assertEqual(False, self.model.is_user_able_to_end(user))

    def test_is_user_able_to_end_when_user_has_no_access(self):
        """is_user_able_to_start should return False if state is ended"""
        self.model.state = 'running'
        user = MagicMock()
        user.has_access_to_route.return_value = False

        self.assertEqual(False, self.model.is_user_able_to_end(user))
        user.has_access_to_route.assert_called_once_with('convent:end')
