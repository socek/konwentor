from pytest import raises
from mock import MagicMock

from hatak.testing import ModelFixture

from ..models import Convent


class TestConvent(ModelFixture):

    def _get_model_class(self):
        return Convent

    def test_states(self, model):
        """Getting and settings states"""
        model.state = 'running'
        assert model.state == 'running'

    def test_state_fail(self, model):
        """Setting invalid state should raise runtimeerror"""
        def method():
            model.state = 'invalid'

        with raises(RuntimeError):
            method()

    def test_is_user_able_to_start_true(self, model):
        """is_user_able_to_start should return True if state is not started and
        user has access to convent:start controller."""
        model.state = 'not started'
        user = MagicMock()
        user.has_access_to_route.return_value = True

        assert model.is_user_able_to_start(user) is True
        user.has_access_to_route.assert_called_once_with('convent:start')

    def test_is_user_able_to_start_when_state_is_running(self, model):
        """is_user_able_to_start should return False if state is running"""
        model.state = 'running'
        user = MagicMock()
        user.has_access_to_route.return_value = True

        assert model.is_user_able_to_start(user) is False

    def test_is_user_able_to_start_when_user_has_no_access(self, model):
        """is_user_able_to_start should return False user has no access to
        convent:start"""
        model.state = 'not started'
        user = MagicMock()
        user.has_access_to_route.return_value = False

        assert model.is_user_able_to_start(user) is False
        user.has_access_to_route.assert_called_once_with('convent:start')

    def test_is_user_able_to_end_true(self, model):
        """is_user_able_to_end should return True if state is running and
        user has access to convent:start controller."""
        model.state = 'running'
        user = MagicMock()
        user.has_access_to_route.return_value = True

        assert model.is_user_able_to_end(user) is True
        user.has_access_to_route.assert_called_once_with('convent:end')

    def test_is_user_able_to_end_when_state_is_ended(self, model):
        """is_user_able_to_start should return False if state is ended"""
        model.state = 'ended'
        user = MagicMock()
        user.has_access_to_route.return_value = True

        assert model.is_user_able_to_end(user) is False

    def test_is_user_able_to_end_when_user_has_no_access(self, model):
        """is_user_able_to_start should return False if state is ended"""
        model.state = 'running'
        user = MagicMock()
        user.has_access_to_route.return_value = False

        assert model.is_user_able_to_end(user) is False
        user.has_access_to_route.assert_called_once_with('convent:end')

    def test_repr(self, model):
        """repr should return name of model"""
        model.name = 'my name'
        model.id = 12
        assert repr(model) == 'Convent (12): my name'

    def test_repr_when_not_set(self, model):
        """repr should return empty name when name is None"""
        assert repr(model) == 'Convent (None): '
