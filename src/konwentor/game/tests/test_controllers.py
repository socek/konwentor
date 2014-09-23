from hatak.plugins.toster.cases import ControllerTestCase
from hatak.plugins.toster.cases import SqlControllerTestCase
from hatak.plugins.toster.fixtures import fixtures
from mock import MagicMock
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..controllers import GameListController, GameAddController, GameDelete
from ..controllers import GameEditController
from ..forms import GameDeleteForm, GameAddForm, GameEditForm


class GameListControllerTests(ControllerTestCase):
    prefix_from = GameListController

    def test_make(self):
        self.add_mock_object(self.controller, 'get_games')
        self.add_mock_object(self.controller, 'add_game_forms')

        self.controller.make()

        self.assertEqual(
            self.mocks['get_games'].return_value, self.data['objects'])
        self.assertEqual({}, self.data['forms'])
        self.mocks['add_game_forms'].assert_called_once_with()

    def test_add_game_forms(self):
        """add_game_forms should add form for every game witch was listed"""
        self.add_mock_object(self.controller, 'add_form')
        form = self.mocks['add_form'].return_value
        obj = MagicMock()
        obj.id = 10
        self.data['objects'] = [obj]
        self.data['form_10'] = form
        self.data['forms'] = {}

        self.controller.add_game_forms()

        self.mocks['add_form'].assert_called_once_with(
            GameDeleteForm, name='form_10')
        self.assertEqual(
            form,
            self.data['forms'][10])
        self.assertEqual(
            form.action,
            self.request.route_path.return_value)
        self.request.route_path.assert_called_once_with(
            'game:delete', obj_id=10)
        form.assert_called_once_with({'obj_id': [10, ]})


class GameListSqlControllerTests(SqlControllerTestCase):
    prefix_from = GameListController

    def test_get_games(self):
        """get_games should return all games"""
        games = self.controller.get_games()

        self.assertEqual(
            [
                fixtures['Game']['first'],
                fixtures['Game']['second'],
                fixtures['Game']['third'],
                fixtures['Game']['dynamic1'],
            ],
            games)


class GameAddControllerTests(ControllerTestCase):
    prefix_from = GameAddController

    def setUp(self):
        super().setUp()
        self.add_mock_object(self.controller, 'add_form')
        self.add_mock_object(self.controller, 'redirect')
        self.form = self.mocks['add_form'].return_value

    def test_make(self):
        self.form.return_value = False

        self.controller.make()

        self.mocks['add_form'].assert_called_once_with(GameAddForm)
        self.assertEqual(0, self.mocks['redirect'].call_count)

    def test_make_on_post(self):
        self.form.return_value = True

        self.controller.make()

        self.mocks['add_form'].assert_called_once_with(GameAddForm)
        self.mocks['redirect'].assert_called_once_with('game:list')


class GameDeleteControllerTests(ControllerTestCase):
    prefix_from = GameDelete

    def setUp(self):
        super().setUp()
        self.add_mock_object(self.controller, 'add_form')
        self.add_mock_object(self.controller, 'redirect')
        self.form = self.mocks['add_form'].return_value

    def test_make(self):
        self.add_mock_object(self.controller, 'get_element')
        self.form.return_value = False
        self.matchdict['obj_id'] = 15

        self.controller.make()

        self.mocks['get_element'].assert_called_once_with()
        self.mocks['add_form'].assert_called_once_with(GameDeleteForm)
        self.form.assert_called_once_with({'obj_id': 15})
        self.assertEqual(0, self.mocks['redirect'].call_count)

    def test_make_on_post(self):
        self.add_mock_object(self.controller, 'get_element')
        self.form.return_value = True
        self.matchdict['obj_id'] = 15

        self.controller.make()

        self.mocks['get_element'].assert_called_once_with()
        self.mocks['add_form'].assert_called_once_with(GameDeleteForm)
        self.form.assert_called_once_with({'obj_id': 15})
        self.mocks['redirect'].assert_called_once_with('game:list')

    def test_get_element_on_error(self):
        """get_element should raise HTTPNotFound exception when no Game found
        """
        self.query.side_effect = NoResultFound()
        self.assertRaises(HTTPNotFound, self.controller.get_element)


class GameDeleteSqlControllerTests(SqlControllerTestCase):
    prefix_from = GameDelete

    def test_get_element(self):
        self.matchdict = self.controller.matchdict = {}
        self.matchdict['obj_id'] = fixtures['Game']['first'].id

        self.controller.get_element()

        obj = self.data['element']
        self.assertEqual(fixtures['Game']['first'], obj)


class GameEditControllerTests(ControllerTestCase):
    prefix_from = GameEditController

    def setUp(self):
        super().setUp()
        self.matchdict['obj_id'] = '10'
        self.add_mock_object(self.controller, 'add_form', auto_spec=True)
        self.form = self.mocks['add_form'].return_value
        self.add_mock_object(self.controller, 'redirect', auto_spec=True)
        self.add_mock_object(self.controller, 'get_game')
        self.game = self.mocks['get_game'].return_value
        self.defaults = {
            'id': [self.game.id],
            'name': [self.game.name],
            'players_description': [self.game.players_description],
            'time_description': [self.game.time_description],
            'type_description': [self.game.type_description],
            'difficulty': [self.game.difficulty],
        }

    def test_make_success(self):
        """GameEdit should add GameEditForm form and redirect to
        game:list if the form is successed"""
        self.form.return_value = True

        self.controller.make()

        self.form.assert_called_once_with(self.defaults)
        self.mocks['add_form'].assert_called_once_with(GameEditForm)
        self.mocks['redirect'].assert_called_once_with('game:list')

    def test_make_fail(self):
        """GameEdit should add GameAddForm form  and do nothing
        if the form is failed or not used"""
        self.form.return_value = False

        self.controller.make()

        self.form.assert_called_once_with(self.defaults)
        self.mocks['add_form'].assert_called_once_with(GameEditForm)
        self.assertFalse(self.mocks['redirect'].called)


class SqlGameEditControllerTests(SqlControllerTestCase):
    prefix_from = GameEditController

    def test_get_game_when_game_exists(self):
        game = fixtures['Game']['first']
        self.matchdict['obj_id'] = str(game.id)

        result = self.controller.get_game()

        self.assertEqual(game, self.data['game'])
        self.assertEqual(game, result)

    def test_get_game_when_game_not_exists(self):
        self.matchdict['obj_id'] = '1231231231231124'

        self.assertRaises(HTTPNotFound, self.controller.get_game)

    def test_get_game_when_game_is_inactive(self):
        game = fixtures['Game']['inactive']
        self.matchdict['obj_id'] = str(game.id)

        self.assertRaises(HTTPNotFound, self.controller.get_game)
