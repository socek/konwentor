from hatak.testing import ControllerFixture, DatabaseFixture
from mock import patch, MagicMock
from pyramid.httpexceptions import HTTPNotFound
from pytest import fixture, raises, yield_fixture
from sqlalchemy.orm.exc import NoResultFound

from konwentor.application.tests.fixtures import Fixtures
from ..controllers import GameListController, GameAddController, GameDelete
from ..controllers import GameEditController
from ..forms import GameDeleteForm, GameAddForm, GameEditForm


class TestGameListController(ControllerFixture):

    def get_controller_class(self):
        return GameListController

    @yield_fixture()
    def get_games(self, controller):
        with patch.object(controller, 'get_games') as mock:
            yield mock

    @yield_fixture()
    def add_game_forms(self, controller):
        with patch.object(controller, 'add_game_forms') as mock:
            yield mock

    @yield_fixture()
    def add_form(self, controller):
        with patch.object(controller, 'add_form') as mock:
            yield mock

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


# class GameListSqlControllerTests(SqlControllerTestCase):
#     prefix_from = GameListController

#     def test_get_games(self):
#         """get_games should return all games"""
#         games = self.controller.get_games()

#         self.assertEqual(
#             [
#                 fixtures['Game']['first'],
#                 fixtures['Game']['second'],
#                 fixtures['Game']['third'],
#                 fixtures['Game']['dynamic1'],
#             ],
#             games)


# class GameAddControllerTests(ControllerTestCase):
#     prefix_from = GameAddController

#     def setUp(self):
#         super().setUp()
#         self.add_mock_object(self.controller, 'add_form')
#         self.add_mock_object(self.controller, 'redirect')
#         self.form = add_form.return_value

#     def test_make(self):
#         self.form.validate.return_value = False

#         self.controller.make()

#         add_form.assert_called_once_with(GameAddForm)
#         self.assertEqual(0, self.mocks['redirect'].call_count)

#     def test_make_on_post(self):
#         self.form.validate.return_value = True

#         self.controller.make()

#         add_form.assert_called_once_with(GameAddForm)
#         self.mocks['redirect'].assert_called_once_with('game:list')


# class GameDeleteControllerTests(ControllerTestCase):
#     prefix_from = GameDelete

#     def setUp(self):
#         super().setUp()
#         self.add_mock_object(self.controller, 'add_form')
#         self.add_mock_object(self.controller, 'redirect')
#         self.form = add_form.return_value

#     def test_make(self):
#         self.add_mock_object(self.controller, 'get_element')
#         self.form.validate.return_value = False
#         self.matchdict['obj_id'] = 15

#         self.controller.make()

#         self.mocks['get_element'].assert_called_once_with()
#         add_form.assert_called_once_with(GameDeleteForm)
#         self.form.set_value('obj_id', 15)
#         self.form.validate.assert_called_once_with()
#         self.assertEqual(0, self.mocks['redirect'].call_count)

#     def test_make_on_post(self):
#         self.add_mock_object(self.controller, 'get_element')
#         self.form.validate.return_value = True
#         self.matchdict['obj_id'] = 15

#         self.controller.make()

#         self.mocks['get_element'].assert_called_once_with()
#         add_form.assert_called_once_with(GameDeleteForm)
#         self.form.set_value.assert_called_once_with('obj_id', 15)
#         self.form.validate.assert_called_once_with()
#         self.mocks['redirect'].assert_called_once_with('game:list')

#     def test_get_element_on_error(self):
#         """get_element should raise HTTPNotFound exception when no Game found
#         """
#         self.query.side_effect = NoResultFound()
#         self.assertRaises(HTTPNotFound, self.controller.get_element)


# class GameDeleteSqlControllerTests(SqlControllerTestCase):
#     prefix_from = GameDelete

#     def test_get_element(self):
#         self.matchdict = self.controller.matchdict = {}
#         self.matchdict['obj_id'] = fixtures['Game']['first'].id

#         self.controller.get_element()

#         obj = self.data['element']
#         self.assertEqual(fixtures['Game']['first'], obj)


# class GameEditControllerTests(ControllerTestCase):
#     prefix_from = GameEditController

#     def setUp(self):
#         super().setUp()
#         self.matchdict['obj_id'] = '10'
#         self.add_mock_object(self.controller, 'add_form', auto_spec=True)
#         self.form = add_form.return_value
#         self.add_mock_object(self.controller, 'redirect', auto_spec=True)
#         self.add_mock_object(self.controller, 'get_game')
#         self.game = self.mocks['get_game'].return_value
#         self.defaults = {
#             'id': self.game.id,
#             'name': self.game.name,
#             'players_description': self.game.players_description,
#             'time_description': self.game.time_description,
#             'type_description': self.game.type_description,
#             'difficulty': self.game.difficulty,
#         }

#     def test_make_success(self):
#         """
#         GameEdit should add GameEditForm form and redirect to
#         game:list if the form is successed
#         """
#         self.form.validate.return_value = True

#         self.controller.make()

#         self.form.parse_dict.assert_called_once_with(self.defaults)
#         self.form.validate.assert_called_once_with()
#         add_form.assert_called_once_with(GameEditForm)
#         self.mocks['redirect'].assert_called_once_with('game:list')

#     def test_make_fail(self):
#         """GameEdit should add GameAddForm form  and do nothing
#         if the form is failed or not used"""
#         self.form.validate.return_value = False

#         self.controller.make()

#         self.form.parse_dict.assert_called_once_with(self.defaults)
#         self.form.validate.assert_called_once_with()
#         add_form.assert_called_once_with(GameEditForm)
#         self.assertFalse(self.mocks['redirect'].called)


class TestsSqlGameEditCntroller(ControllerFixture, DatabaseFixture):

    def get_controller_class(self):
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

    def test_get_game_when_game_not_exists(self, matchdict, controller):
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
