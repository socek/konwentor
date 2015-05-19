from pytest import yield_fixture
from mock import patch, MagicMock

from konwentor.application.testing import ControllerFixture
from ..controllers import AuthListController, AuthEditController
from ..forms import AuthEditForm


class TestAuthListController(ControllerFixture):

    def _get_controller_class(self):
        return AuthListController

    @yield_fixture
    def UserWidget(self):
        patcher = patch('konwentor.auth.controllers.UserWidget')
        with patcher as mock:
            yield mock

    def test_make(self, controller, UserWidget, mdriver, data, request):
        """
        .make should add list of all users wich are decorated with UserWidget
        """
        user = MagicMock()
        mdriver.Auth.find_all.return_value = [user]

        controller.make()

        assert list(data['users']) == [UserWidget.return_value]
        UserWidget.assert_called_once_with(request, user)


class TestAuthEditController(ControllerFixture):

    def _get_controller_class(self):
        return AuthEditController

    @yield_fixture
    def get_user(self, controller):
        patcher = patch.object(controller, 'get_user')
        with patcher as mock:
            yield mock

    def test_when_form_is_not_validated(
        self,
        controller,
        add_form,
        form,
        get_user
    ):
        """
        .make should fill form with user data
        """
        form.validate.return_value = False

        controller.make()

        get_user.assert_called_once_with()
        add_form.assert_called_once_with(AuthEditForm)
        form.fill.assert_called_once_with(get_user.return_value)

    def test_when_form_is_validated(
        self,
        controller,
        add_form,
        form,
        get_user,
        mdb,
        add_flashmsg,
        redirect,
    ):
        """
        .make should commit, add flash message and redirect when forms is
        validated successfully
        """
        form.validate.return_value = True

        controller.make()

        get_user.assert_called_once_with()
        add_form.assert_called_once_with(AuthEditForm)
        assert form.fill.called is False
        mdb.commit.assert_called_once_with()
        add_flashmsg.assert_called_once_with(
            'Użytkownik został zapisany!',
            'info'
        )
        redirect.assert_called_once_with('auth:list')

    def test_get_user(self, controller, mdriver, matchdict):
        """
        .get_user should return user wich id is parsed from url
        """
        matchdict['obj_id'] = '123'

        assert controller.get_user() == mdriver.Auth.get_by_id.return_value

        mdriver.Auth.get_by_id.assert_called_once_with('123')
