from mock import MagicMock, call
from sqlalchemy.orm.exc import NoResultFound

from haplugin.toster import ControllerTestCase, SqlControllerTestCase
from haplugin.toster.fixtures import fixtures

from ..controllers import EndController
from ..controllers import GameCopyAddController, GameCopyToBoxController
from ..controllers import GameCopyControllerBase, GameCopyListController
from konwentor.convent.helpers import ConventWidget
from konwentor.gamecopy.forms import GameCopyAddForm


class GameCopyControllerBaseTests(ControllerTestCase):
    prefix_from = GameCopyControllerBase

    def test_verify_convent_false(self):
        """verify_convent should return False when convent_id is not in
        session"""
        self.add_mock_object(self.controller, 'add_flashmsg', autospec=True)
        self.add_mock_object(self.controller, 'redirect', autospec=True)
        self.controller.session = {}

        self.assertEqual(False, self.controller.verify_convent())
        self.mocks['add_flashmsg'].assert_called_once_with(
            'Proszę wybrać konwent.', 'danger')
        self.mocks['redirect'].assert_called_once_with('convent:list')

    def test_verify_convent_true(self):
        """verify_convent should return True when convent_id is in session"""
        self.controller.session = {
            'convent_id': 1,
        }

        self.assertEqual(True, self.controller.verify_convent())

    def test_make_helpers(self):
        """make_helpers should add ConventWidget helper"""
        self.add_mock_object(self.controller, 'add_helper', autospec=True)
        self.add_mock_object(self.controller, 'get_convent', autospec=True)

        self.controller.make_helpers()

        self.mocks['add_helper'].assert_called_once_with(
            'convent',
            ConventWidget,
            self.mocks['get_convent'].return_value,
        )


class GameCopyControllerBaseSqlTests(SqlControllerTestCase):
    prefix_from = GameCopyControllerBase

    def test_get_convent(self):
        """get_convent should return convent which id is saved in session."""
        convent = fixtures['Convent']['first']
        self.controller.session = {
            'convent_id': convent.id,
        }

        result = self.controller.get_convent()

        self.assertEqual(convent, result)

    def test_get_convent_on_inactive_convent(self):
        """get_convent should raise NoResultFound when convent is inactive"""
        self.add_mock_object(self.controller, 'add_flashmsg')
        self.add_mock_object(self.controller, 'redirect')

        convent = fixtures['Convent']['inactive']
        self.controller.session = {
            'convent_id': convent.id,
        }

        self.assertRaises(EndController, self.controller.get_convent)
        self.mocks['add_flashmsg'].assert_called_once_with(
            'Proszę wybrać konwent.', 'danger')
        self.mocks['redirect'].assert_called_once_with('convent:list')


class GameCopyListControllerTestCase(SqlControllerTestCase):
    prefix_from = GameCopyListController

    def test_get_games(self):
        """get_games should return list of games avalible on convent"""
        convent = fixtures['Convent']['first']
        result = self.controller.get_games(convent)

        self.assertEqual(3, len(result))
        for element in result:
            self.assertEqual(convent, element.GameEntity.convent)


class GameCopyAddControllerTests(ControllerTestCase):
    prefix_from = GameCopyAddController

    def setUp(self):
        super().setUp()
        self.add_mock_object(self.controller, 'verify_convent')
        self.mocks['verify_convent'].return_value = True
        self.add_mock_object(self.controller, 'add_form')
        self.add_mock_object(self.controller, 'add_flashmsg')

    def test_verify_convent(self):
        """Controller should do nothing if verify_convent fails"""
        self.mocks['verify_convent'].return_value = False

        self.controller.make()

        self.mocks['verify_convent'].assert_called_once_with()
        self.assertEqual(0, self.mocks['add_form'].call_count)

    def test_form_not_submitted(self):
        """Controller should create form after verify_convent check."""
        form = self.mocks['add_form'].return_value
        form.validate.return_value = None

        self.controller.make()

        self.mocks['add_form'].assert_called_once_with(GameCopyAddForm)
        form.validate.assert_called_once_with()
        form.parse_dict({
            'count': 1,
            'user_id': self.user.id,
            'convent_id': self.session['convent_id'],
        })
        self.assertEqual(0, self.mocks['add_flashmsg'].call_count)

    def test_form_submitted(self):
        self.session = self.controller.session = {
            'last_convent_id': 1,
            'last_user_id': -1,
            'convent_id': 2
        }
        form = self.mocks['add_form'].return_value
        form.validate.return_value = True

        self.controller.make()

        self.mocks['add_form'].assert_called_once_with(GameCopyAddForm)
        form.validate.assert_called_once_with()
        form.parse_dict.assert_called_once_with({
            'count': 1,
            'user_id': -1,
            'convent_id': 1,
        })

        self.mocks['add_flashmsg'].assert_called_once_with(
            'Dodano grę.', 'info')

        form.get_value.assert_has_calls([
            call('convent_id'),
            call('user_id'),
        ])
        self.assertEqual(
            form.get_value.return_value,
            self.session['last_convent_id'],
        )
        self.assertEqual(
            form.get_value.return_value,
            self.session['last_user_id'],
        )


class GameCopyListControllerTests(ControllerTestCase):
    prefix_from = GameCopyListController

    def setUp(self):
        super().setUp()
        self.add_mock_object(self.controller, 'verify_convent')
        self.mocks['verify_convent'].return_value = True

    def test_verify_convent(self):
        """Controller should do nothing if verify_convent fails"""
        self.mocks['verify_convent'].return_value = False

        self.controller.make()

        self.mocks['verify_convent'].assert_called_once_with()
        self.assertEqual({}, self.data)

    def test_normal(self):
        game = MagicMock()
        self.add_mock_object(self.controller, 'get_convent')
        self.add_mock_object(self.controller, 'get_games', return_value=[game])
        self.add_mock('GameEntityWidget')

        self.controller.make()

        self.mocks['verify_convent'].assert_called_once_with()
        self.assertEqual({
            'convent': self.mocks['get_convent'].return_value,
            'games': [self.mocks['GameEntityWidget'].return_value],
        }, self.data)
        self.mocks['get_games'].assert_called_once_with(
            self.mocks['get_convent'].return_value)
        self.mocks['GameEntityWidget'].assert_called_once_with(
            self.request,
            game)


class GameCopyToBoxControllerTests(ControllerTestCase):
    prefix_from = GameCopyToBoxController

    def setUp(self):
        super().setUp()
        self.add_mock_object(self.controller, 'verify_convent')
        self.add_mock_object(self.controller, 'redirect')
        self.add_mock_object(self.controller, 'add_flashmsg')

    def test_make_bad_convent_id(self):
        """GameCopyToBoxController should verify convent and do nothing if it
        fails"""
        self.mocks['verify_convent'].return_value = False

        self.controller.make()

        self.mocks['verify_convent'].assert_called_once_with()
        self.assertEqual(0, self.mocks['add_flashmsg'].call_count)
        self.assertEqual(0, self.mocks['redirect'].call_count)

    def test_make(self):
        """GameCopyToBoxController should verify convent, move game copy to box
        and redirect to gamecopy:list"""
        self.add_mock_object(self.controller, 'move_to_box')
        self.mocks['verify_convent'].return_value = True

        self.controller.make()

        self.mocks['verify_convent'].assert_called_once_with()

        self.mocks['move_to_box'].assert_called_once_with()
        self.mocks['add_flashmsg'].assert_called_once_with(
            'Gra została schowana.', 'success')
        self.mocks['redirect'].assert_called_once_with('gamecopy:list')

    def test_move_to_box(self):
        """move_to_box should get entity, move it to box and commit to db."""
        self.add_mock_object(self.controller, 'get_game_entity')
        self.add_mock_object(self.controller, 'get_convent')

        self.controller.move_to_box()

        self.mocks['get_convent'].assert_called_once_with()
        convent = self.mocks['get_convent'].return_value
        self.mocks['get_game_entity'].assert_called_once_with(convent)
        entity = self.mocks['get_game_entity'].return_value
        entity.move_to_box.assert_called_once_with()
        self.db.commit.assert_called_once_with()


class SqlGameCopyToBoxControllerTests(SqlControllerTestCase):
    prefix_from = GameCopyToBoxController

    def test_get_game_entity(self):
        """get_game_entity should return return GameEntity which id is provided
        by matchdict and convent do match."""
        entity = fixtures['GameEntity'][0]
        convent = entity.convent
        self.matchdict['obj_id'] = entity.id

        result = self.controller.get_game_entity(convent)

        self.assertEqual(entity, result)

    def test_game_entity_when_convent_does_not_match(self):
        """get_game_entity should raises () when convent does not match"""
        entity = fixtures['GameEntity'][0]
        convent = fixtures['Convent']['second']
        self.matchdict['obj_id'] = entity.id

        self.assertRaises(
            NoResultFound,
            self.controller.get_game_entity,
            convent)
