from mock import MagicMock, call

from haplugin.toster import FormTestCase, SqlFormTestCase, TestCase
from haplugin.toster import SqlTestCase
from haplugin.toster.fixtures import fixtures
from sqlalchemy.orm.exc import NoResultFound

from ..forms import GameBorrowAddForm, GameBorrowReturnForm
from ..forms import IsGameBorrowExisting


class GameBorrowAddFormTest(FormTestCase):
    prefix_from = GameBorrowAddForm

    def setUp(self):
        super().setUp()
        self.add_mock_object(self.form, 'get_entity')
        self.entity = self.mocks['get_entity'].return_value

    def test_get_avalible_documents(self):
        elements = self.form.get_avalible_documents()
        self.assertEqual({
            'label': '(Wybierz)',
            'value': '',
        }, elements[0])

    def test_overal_validation(self):
        """overalValidation should return GameEntity.is_avalible"""
        self.entity.is_avalible.return_value = True

        self.assertEqual(
            True,
            self.form.overal_validation({'game_entity_id': ['1']}))

        self.mocks['get_entity'].assert_called_once_with('1')

    def test_overal_validation_false(self):
        """overalValidation should return GameEntity.is_avalible"""
        self.entity.is_avalible.return_value = False

        self.assertEqual(
            False,
            self.form.overal_validation({'game_entity_id': ['1']}))

        self.mocks['get_entity'].assert_called_once_with('1')
        self.assertEqual(
            'Ta gra nie ma już wolnych kopii.',
            self.form.message)

    def test_submit(self):
        self.add_mock('GameBorrow')

        self.form.parse_dict({
            'game_entity_id': [12],
            'name': ['sds'],
            'surname': ['zxc'],
            'document_type': ['ccs'],
            'document_number': ['wer'],
        })
        self.form.submit()

        element = self.mocks['GameBorrow'].return_value

        self.assertEqual(12, element.game_entity_id)
        self.assertEqual('sds', element.name)
        self.assertEqual('zxc', element.surname)
        self.assertEqual(True, element.is_borrowed)
        element.set_document.assert_called_once_with('ccs', 'wer')

        self.db.add.assert_called_once_with(element)
        self.db.commit.assert_called_once_with()


class SqlGameBorrowAddFormTest(SqlFormTestCase):
    prefix_from = GameBorrowAddForm

    def test_get_entity(self):
        _id = fixtures['GameEntity'][0].id
        entity = self.form.get_entity(_id)

        self.assertEqual(
            fixtures['GameEntity'][0],
            entity)


class SqlGameBorrowReturnFormTest(SqlFormTestCase):
    prefix_from = GameBorrowReturnForm

    def test_get_avalible_games(self):
        self.form.set_value('convent_id', fixtures['Convent']['first'].id)

        result = list(self.form.get_avalible_games())

        self.assertEqual(2, len(result))
        self.assertEqual(2, result[0].GameEntity.id)
        self.assertEqual(3, result[1].GameEntity.id)


class GameBorrowReturnFormTest(FormTestCase):
    prefix_from = GameBorrowReturnForm

    def setUp(self):
        super().setUp()
        self.add_mock_object(self.form, 'get_avalible_games')
        self.obj = MagicMock()
        self.obj.name = 'name'
        self.obj.User.name = 'owner'
        self.mocks['get_avalible_games'].return_value = [self.obj]

    def test_get_entity_ids(self):
        self.assertEqual(
            ['', str(self.obj.GameEntity.id)],
            list(self.form.get_entity_ids()))

    def test_get_game_names_for_select(self):
        self.assertEqual(
            [
                {
                    'value': '',
                    'label': '(nie wypożycza)'
                },
                {
                    'value': self.obj.GameEntity.id,
                    'label': 'owner - name'
                }
            ],
            list(self.form.get_game_names_for_select()))

    def test_submit(self):
        self.add_mock_object(self.form, 'return_game')
        self.add_mock_object(self.form, 'borrow_next')

        self.form.submit()

        self.mocks['return_game'].assert_called_once_with()
        self.mocks['borrow_next'].assert_called_once_with()
        self.form.db.flush.assert_called_once_with()
        self.form.db.commit.assert_called_once_with()

    def test_return_game(self):
        self.add_mock('datetime')
        self.form.borrow = MagicMock()

        self.form.return_game()

        self.assertEqual(False, self.form.borrow.is_borrowed)
        self.assertEqual(
            self.mocks['datetime'].utcnow.return_value,
            self.form.borrow.return_timestamp)

    def test_borrow_next_whit_empty_game_entity_id(self):
        self.add_mock_object(self.form, 'get_value')
        self.mocks['get_value'].return_value = None

        self.form.borrow_next()

        self.mocks['get_value'].assert_called_once_with('game_entity_id')

    def test_borrow_next(self):
        self.add_mock_object(self.form, 'get_value')
        borrow = self.form.borrow = MagicMock()
        self.mocks['get_value'].return_value = 123
        self.add_mock('GameBorrow')
        self.add_mock('datetime')

        self.form.borrow_next()

        self.mocks['get_value'].assert_has_calls([
            call('game_entity_id'),
            call('game_entity_id'),
        ])
        self.mocks['GameBorrow'].assert_called_once_with()
        obj = self.mocks['GameBorrow'].return_value
        self.assertEqual(obj, self.form.new_borrow)

        obj.assign_request.assert_called_once_with(self.request)
        self.assertEqual(123, obj.game_entity_id)
        self.assertEqual(borrow.name, obj.name)
        self.assertEqual(obj.surname, borrow.surname)
        self.assertEqual(obj.stats_hash, borrow.stats_hash)
        self.assertEqual(obj.is_borrowed, True)
        self.assertEqual(
            self.mocks['datetime'].utcnow.return_value,
            obj.borrowed_timestamp)
        self.form.db.add.assert_called_once_with(obj)


class IsGameBorrowExistingTest(TestCase):
    prefix_from = IsGameBorrowExisting

    def setUp(self):
        super().setUp()
        self.validator = self.prefix_from()
        self.form = MagicMock()
        self.validator.set_form(self.form)
        self.add_mock_object(self.validator, 'get_borrow')

    def test_validate_fail(self):
        self.mocks['get_borrow'].side_effect = NoResultFound

        self.assertEqual(False, self.validator.validate())
        self.form.get_value.assert_called_once_with('game_borrow_id')
        self.mocks['get_borrow'].assert_called_once_with(
            self.form.get_value.return_value)

    def test_validate_success(self):
        self.assertEqual(True, self.validator.validate())
        self.form.get_value.assert_called_once_with('game_borrow_id')
        self.mocks['get_borrow'].assert_called_once_with(
            self.form.get_value.return_value)
        self.assertEqual(
            self.mocks['get_borrow'].return_value,
            self.form.borrow)


class SqlIsGameBorrowExistingTest(SqlTestCase):
    prefix_from = IsGameBorrowExisting

    def setUp(self):
        super().setUp()
        self.validator = self.prefix_from()
        self.form = MagicMock()
        self.validator.set_form(self.form)
        self.form.query = self.db.query

    def test_get_borrow(self):
        borrow = self.validator.get_borrow(fixtures['GameBorrow'][0].id)

        self.assertEqual(borrow, fixtures['GameBorrow'][0])
