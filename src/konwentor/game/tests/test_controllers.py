from pytest import fixture, raises, yield_fixture
from mock import patch, MagicMock
from sqlalchemy.orm.exc import NoResultFound
from pyramid.httpexceptions import HTTPNotFound

from ..controllers import GameListController, GameAddController, GameDelete
from ..controllers import GameEditController
from ..forms import GameDeleteForm, GameAddForm, GameEditForm
from konwentor.application.testing import ControllerFixture


class LocalFixtures(ControllerFixture):

    @yield_fixture
    def get_games(self, controller):
        with patch.object(controller, 'get_games') as mock:
            yield mock

    @yield_fixture
    def add_game_forms(self, controller):
        with patch.object(controller, 'add_game_forms') as mock:
            yield mock

    @yield_fixture
    def get_element(self, controller):
        patcher = patch.object(controller, 'get_element')
        with patcher as mock:
            yield mock

    @fixture
    def form(self, add_form):
        return add_form.return_value


class TestGameListController(LocalFixtures):

    def _get_controller_class(self):
        return GameListController

    def test_make(self, controller, data, get_games, add_game_forms):
        controller.make()

        assert get_games.return_value == data['objects']
        assert {} == data['forms']
        add_game_forms.assert_called_once_with()

    def test_add_game_forms(self, add_form, data, controller, request):
        """add_game_forms should add form for every game witch was listed"""
        form = add_form.return_value

        obj = MagicMock()
        obj.id = 10
        data['objects'] = [obj]
        data['form_10'] = form
        data['forms'] = {}

        controller.add_game_forms()

        add_form.assert_called_once_with(GameDeleteForm, name='form_10')
        assert form == data['forms'][10]
        assert form.action == request.route_path.return_value
        request.route_path.assert_called_once_with('game:delete', obj_id=10)
        form.set_value.assert_called_once_with('obj_id', 10)
        form.validate.assert_called_once_with()

    def test_get_games(self, controller, fixtures):
        """get_games should return all games"""
        games = controller.get_games()

        assert games == [
            fixtures['Game']['first'],
            fixtures['Game']['second'],
            fixtures['Game']['third'],
            fixtures['Game']['dynamic1'],
        ]


class TestGameAddController(LocalFixtures):

    def _get_controller_class(self):
        return GameAddController

    def test_make(self, controller, form, add_form, redirect):
        form.validate.return_value = False

        controller.make()

        add_form.assert_called_once_with(GameAddForm)
        assert not redirect.called

    def test_make_on_post(self, controller, form, add_form, redirect):
        form.validate.return_value = True

        controller.make()

        add_form.assert_called_once_with(GameAddForm)
        redirect.assert_called_once_with('game:list')


class TestGameDeleteController(LocalFixtures):

    def _get_controller_class(self):
        return GameDelete

    def test_make(
        self,
        controller,
        form,
        matchdict,
        add_form,
        redirect,
        get_element,
    ):
        form.validate.return_value = False
        matchdict['obj_id'] = 15

        controller.make()

        get_element.assert_called_once_with()
        add_form.assert_called_once_with(GameDeleteForm)
        form.set_value('obj_id', 15)
        form.validate.assert_called_once_with()
        assert not redirect.called

    def test_make_on_post(
        self,
        controller,
        form,
        matchdict,
        add_form,
        redirect,
        get_element,
    ):
        form.validate.return_value = True
        matchdict['obj_id'] = 15

        controller.make()

        get_element.assert_called_once_with()
        add_form.assert_called_once_with(GameDeleteForm)
        form.set_value.assert_called_once_with('obj_id', 15)
        form.validate.assert_called_once_with()
        redirect.assert_called_once_with('game:list')

    def test_get_element_on_error(self, controller, mdb):
        """
        get_element should raise HTTPNotFound exception when no Game found
        """
        mdb.query.side_effect = NoResultFound()
        with raises(HTTPNotFound):
            controller.get_element()

    def test_get_element(self, controller, matchdict, fixtures, data):
        matchdict['obj_id'] = fixtures['Game']['first'].id

        controller.get_element()

        obj = data['element']
        assert obj == fixtures['Game']['first']


class TestGameEditController(LocalFixtures):

    def _get_controller_class(self):
        return GameEditController

    @fixture
    def matchdict(self):
        data = super().matchdict()
        data['obj_id'] = '10'
        return data

    @yield_fixture
    def get_game(self, controller):
        patcher = patch.object(controller, 'get_game')
        with patcher as mock:
            yield mock

    @fixture
    def game(self, get_game):
        return get_game.return_value

    @fixture
    def defaults(self, game):
        return {
            'id': game.id,
            'name': game.name,
            'players_description': game.players_description,
            'time_description': game.time_description,
            'type_description': game.type_description,
            'difficulty': game.difficulty,
        }

    def test_make_success(
        self,
        controller,
        form,
        add_form,
        redirect,
        defaults,
    ):
        """
        GameEdit should add GameEditForm form and redirect to
        game:list if the form is successed
        """
        form.validate.return_value = True

        controller.make()

        form.parse_dict.assert_called_once_with(defaults)
        form.validate.assert_called_once_with()
        add_form.assert_called_once_with(GameEditForm)
        redirect.assert_called_once_with('game:list')

    def test_make_fail(
        self,
        form,
        controller,
        add_form,
        redirect,
        defaults,
    ):
        """
        GameEdit should add GameAddForm form  and do nothing
        if the form is failed or not used.
        """
        form.validate.return_value = False

        controller.make()

        form.parse_dict.assert_called_once_with(defaults)
        form.validate.assert_called_once_with()
        add_form.assert_called_once_with(GameEditForm)
        assert not redirect.called


class TestsSqlGameEditCntroller(LocalFixtures):

    def _get_controller_class(self):
        return GameEditController

    def test_get_game_when_game_exists(
            self,
            fixtures,
            matchdict,
            data,
            controller,
    ):
        game = fixtures['Game']['first']
        matchdict['obj_id'] = str(game.id)

        result = controller.get_game()

        assert game == data['game']
        assert game == result

    def test_get_game_when_game_not_exists(
        self,
        matchdict,
        controller,
        fixtures,
    ):
        matchdict['obj_id'] = '1231231231231124'

        with raises(HTTPNotFound):
            controller.get_game()

    def test_get_game_when_game_is_inactive(
            self,
            fixtures,
            matchdict,
            controller):
        game = fixtures['Game']['inactive']
        matchdict['obj_id'] = str(game.id)

        with raises(HTTPNotFound):
            controller.get_game()
