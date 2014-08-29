from mock import MagicMock, create_autospec

from hatak.tests.cases import FormTestCase, SqlTestCase
from hatak.tests.fixtures import fixtures

from ..forms import GameCopyAddForm
from ..models import GameCopy, GameEntity
from konwentor.auth.models import User
from konwentor.convent.models import Convent
from konwentor.game.models import Game


class GameCopyAddFormTest(FormTestCase):

    prefix_from = GameCopyAddForm

    def test_get_objects(self):
        """get_objects should return list of dicts"""
        example_model = MagicMock()
        self.query.return_value.all.return_value = [example_model]

        data = self.form.get_objects(self)

        self.assertEqual({
            'label': '(Wybierz)',
            'value': '',
        }, data[0])

        self.assertEqual({
            'label': example_model.name,
            'value': str(example_model.id),
        }, data[1])

        self.query.assert_called_with(self)
        self.query.return_value.all.assert_called_with()

    def test_submit(self):
        """Submit should create gamecopy and gameentity (with count)."""
        self.add_mock('Game')
        self.add_mock('User')
        self.add_mock('Convent')
        self.add_mock_object(self.form, 'create_gamecopy', autospec=True)
        self.add_mock_object(self.form, 'create_gameentity', autospec=True)
        self.mocks['create_gameentity'].return_value.count = 3

        self.form.submit({
            'game_id': ['game_id'],
            'user_id': ['user_id'],
            'convent_id': ['convent_id'],
            'count': ['2'],
        })

        self.mocks['Game'].get_by_id.assert_called_once_with(
            self.db, 'game_id')
        self.mocks['User'].get_by_id.assert_called_once_with(
            self.db, 'user_id')
        self.mocks['Convent'].get_by_id.assert_called_once_with(
            self.db, 'convent_id')

        self.mocks['create_gamecopy'].assert_called_once_with(
            self.mocks['Game'].get_by_id.return_value,
            self.mocks['User'].get_by_id.return_value,
        )

        self.mocks['create_gameentity'].assert_called_once_with(
            self.mocks['Convent'].get_by_id.return_value,
            self.mocks['create_gamecopy'].return_value,
        )
        gameentity = self.mocks['create_gameentity'].return_value

        self.assertEqual(gameentity.count, 5)

        self.db.commit.assert_called_once_with()
        self.db.rollback.assert_called_once_with()

    def test_create_gamecopy(self):
        """create_gamecopy should get or create GameCopy object."""
        self.add_mock('GameCopy')
        game = create_autospec(Game())
        user = create_autospec(User())

        result = self.form.create_gamecopy(game, user)
        self.assertEqual(
            self.mocks['GameCopy'].get_or_create.return_value, result)
        self.mocks['GameCopy'].get_or_create.assert_called_once_with(
            self.db,
            game=game,
            owner=user)
        self.db.add.assert_called_once_with(result)

    def test_create_gameentity(self):
        """create_gameentity should create GameEntity."""
        self.add_mock('GameEntity')
        convent = create_autospec(Convent())
        gamecopy = create_autospec(GameCopy())

        gameentity = self.form.create_gameentity(convent, gamecopy)
        self.assertEqual(
            self.mocks['GameEntity'].get_or_create.return_value, gameentity)
        self.mocks['GameEntity'].get_or_create.assert_called_once_with(
            self.db,
            convent=convent,
            gamecopy=gamecopy)
        self.db.add.assert_called_once_with(gameentity)


class GameCopyAddFormSqlTestCase(SqlTestCase):

    prefix_from = GameCopyAddForm

    def test_success(self):
        """GameCopyAddForm is creating data."""
        self.form = self.prefix_from(self.request)

        game = fixtures['Game']['dynamic1']
        user = fixtures['User']['dynamic1']
        convent = fixtures['Convent']['dynamic1']

        self.request.POST.dict_of_lists.return_value = {
            self.form.form_name_value: [self.form.name, ],
            'game_id': [str(game.id), ],
            'user_id': [str(user.id), ],
            'convent_id': [str(convent.id), ],
            'count': ['5', ],
        }

        self.form()
        self.db.flush()

        entity = (
            self.query(GameEntity)
            .filter(GameEntity.convent == convent)
            .one()
        )
        copy = entity.gamecopy

        self.assertEqual(5, entity.count)
        self.assertEqual(game, copy.game)
        self.assertEqual(user, copy.owner)

        try:
            self.db.delete(copy)
            self.db.delete(entity)
            self.db.commit()
        finally:
            self.db.rollback()
