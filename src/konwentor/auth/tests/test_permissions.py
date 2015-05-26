from pytest import fixture, yield_fixture
from mock import MagicMock, patch

from hatak.testing import RequestFixture

from ..permissions import ListAvaliblePermissions
from ..models import Permission


class TestListAvaliblePermissions(RequestFixture):

    @fixture
    def route(self, request):
        route = MagicMock()
        request.registry = {'route': route}
        return route

    @fixture
    def user(self):
        return MagicMock()

    @fixture
    def model(self, request, route, user):
        return ListAvaliblePermissions(request, user)

    @yield_fixture
    def get_all(self, model):
        patcher = patch.object(model, 'get_all')
        with patcher as mock:
            yield mock

    @yield_fixture
    def get_all_permissions(self, model):
        patcher = patch.object(model, 'get_all_permissions')
        with patcher as mock:
            yield mock

    @yield_fixture
    def is_permission_avalible(self, model):
        patcher = patch.object(model, 'is_permission_avalible')
        with patcher as mock:
            yield mock

    @yield_fixture
    def gather_user_permissions(self, model):
        patcher = patch.object(model, 'gather_user_permissions')
        with patcher as mock:
            yield mock

    def test_is_permission_avalible_when_in_avalible_permissions(
        self,
        model,
    ):
        '''
        .is_permission_avalible should return False if permission is already in
        avalible_permissions set.
        '''
        model.avalible_permissions = set(['group:name'])
        model.user_permissions = set()
        assert model.is_permission_avalible('group:name') is False

    def test_is_permission_avalible_when_in_user_permissions(
        self,
        model,
    ):
        '''
        .is_permission_avalible should return False if permission is already in
        user permissions
        '''
        model.avalible_permissions = set()
        model.user_permissions = set(['group:name'])
        assert model.is_permission_avalible('group:name') is False

    def test_is_permission_avalible(self, model, is_permission_avalible):
        '''
        .is_permission_avalible should return True if permission is not in any
        of sets.
        '''
        is_permission_avalible.return_value = True
        model.avalible_permissions = set()
        model.user_permissions = set()
        assert model.is_permission_avalible('group:name') is True

    def test_get_all_permissions(self, model, route, is_permission_avalible):
        '''
        .get_all_permissions should yield all permissions of all controllers
        in routes and do nothing when no permission found
        '''
        is_permission_avalible.return_value = True
        myroute = MagicMock()
        myroute.permissions = [('one', 'one'), ('two', 'two')]
        route.routes = {'myroute': myroute, 'second': None}

        assert list(model.get_all_permissions()) == ['one:one', 'two:two']

    def test_get_all_permissions_when_permission_is_not_avalible(
        self,
        model,
        route,
        is_permission_avalible,
    ):
        '''
        .get_all_permissions should not yield permissions which are not
        avalible.
        '''
        is_permission_avalible.return_value = False
        myroute = MagicMock()
        myroute.permissions = [('one', 'one'), ('two', 'two')]
        route.routes = {'myroute': myroute, 'second': None}

        assert list(model.get_all_permissions()) == []

    def test_gather_user_permissions(self, model, user):
        '''
        .gather_user_permissions should make permissions set from user
        permissions
        '''
        user.permissions = [
            Permission(group='group1', name='name1'),
            Permission(group='group2', name='name2'),
        ]

        model.gather_user_permissions()

        assert model.user_permissions == set(['group1:name1', 'group2:name2'])

    def test_gather_user_permission_when_no_user_set(self, model):
        '''
        .gather_user_permissions should leave mepty user_permissions set when
        no user was provided
        '''
        model.user = None

        model.gather_user_permissions()

        assert model.user_permissions == set()

    def test_get_all(
        self,
        model,
        gather_user_permissions,
        get_all_permissions,
    ):
        get_all_permissions.return_value = ['g1:n2']

        assert list(model.get_all()) == ['g1:n2']
        assert model.avalible_permissions == set(['g1:n2'])
