from haplugin.toster import ControllerTestCase, SqlControllerTestCase
from haplugin.toster.fixtures import fixtures
from mock import MagicMock
from pyramid.httpexceptions import HTTPNotFound

from ..controllers import GameBorrowAddController, GameBorrowListController
from ..controllers import GameBorrowReturnController, ShowPersonHint
from konwentor.gameborrow.models import make_hash_document
from konwentor.application.init import main


class GameBorrowAddControllerTests(ControllerTestCase):
    prefix_from = GameBorrowAddController

    def setUp(self):
        super().setUp()
        self.add_mock_object(self.controller, 'get_game_entity')
        self.add_mock_object(self.controller, 'add_form')
        self.add_mock_object(self.controller, 'add_flashmsg')
        self.add_mock_object(self.controller, 'redirect')
        self.form = self.mocks['add_form'].return_value

    def test_make(self):
        self.form.return_value = False

        self.controller.make()

        self.assertEqual(
            self.mocks['get_game_entity'].return_value,
            self.data['game_entity'])
        self.form.set_value('game_entity_id', self.data['game_entity'].id)
        self.form.assert_called_once_with()
        self.assertEqual(0, self.mocks['add_flashmsg'].call_count)
        self.assertEqual(0, self.mocks['redirect'].call_count)

    def test_make_on_form(self):
        self.form.return_value = True

        self.controller.make()

        self.assertEqual(
            self.mocks['get_game_entity'].return_value,
            self.data['game_entity'])
        self.form.set_value.assert_called_once_with(
            'game_entity_id',
            self.data['game_entity'].id)
        self.form.assert_called_once_with()
        self.mocks['add_flashmsg'].assert_called_once_with(
            'Gra została wypożyczona.', 'success')
        self.mocks['redirect'].assert_called_once_with('gamecopy:list')


class SqlGameBorrowAddControllerTests(SqlControllerTestCase):
    prefix_from = GameBorrowAddController

    def test_get_game_entity(self):
        """get_game_entity should return GameEntity with id get from
        matchdict['obj_id']"""
        self.matchdict['obj_id'] = fixtures['GameEntity'][0].id

        entity = self.controller.get_game_entity()

        self.assertEqual(fixtures['GameEntity'][0], entity)

    def test_get_game_entity_not_found(self):
        """get_game_entity should raise HTTPNotFound when no GameEntity found
        """
        self.matchdict['obj_id'] = 21321312

        self.assertRaises(HTTPNotFound, self.controller.get_game_entity)


class GameBorrowListControllerTests(ControllerTestCase):
    prefix_from = GameBorrowListController

    def setUp(self):
        super().setUp()
        self.add_mock_object(self.controller, 'verify_convent')
        self.add_mock_object(self.controller, 'get_convent')
        self.add_mock_object(self.controller, 'get_borrows')
        self.add_mock_object(self.controller, 'generate_log')

    def test_make_no_convent(self):
        """GameBorrowListController should do nothing when no convent found"""
        self.mocks['verify_convent'].return_value = False

        self.controller.make()

        self.mocks['verify_convent'].assert_called_once_with()
        self.assertEqual(0, self.mocks['get_convent'].call_count)
        self.assertEqual(0, self.mocks['get_borrows'].call_count)
        self.assertEqual(0, self.mocks['generate_log'].call_count)

    def test_make(self):
        self.mocks['verify_convent'].return_value = True

        self.controller.make()

        self.mocks['verify_convent'].assert_called_once_with()
        self.mocks['get_convent'].assert_called_once_with()
        self.mocks['get_borrows'].assert_called_once_with(self.data['convent'])
        self.mocks['generate_log'].assert_called_once_with(
            self.data['convent'])

        self.assertEqual(
            self.mocks['get_convent'].return_value,
            self.data['convent'])
        self.assertEqual(
            self.mocks['get_borrows'].return_value,
            self.data['borrows'])
        self.assertEqual(
            self.mocks['generate_log'].return_value,
            self.data['logs'])


class SqlGameBorrowListControllerTests(SqlControllerTestCase):
    prefix_from = GameBorrowListController

    def test_get_borrows(self):
        """get_borrows should return all active borrows"""
        entities = self.controller.get_borrows(fixtures['Convent']['first'])
        self.assertEqual(
            [fixtures['GameBorrow'][0], fixtures['GameBorrow'][1]],
            entities)

    def test_generate_log(self):
        """generate_log should return all non active borrows"""
        entities = self.controller.generate_log(fixtures['Convent']['first'])
        self.assertEqual(
            [fixtures['GameBorrow'][2]],
            entities)


class GameBorrowReturnControllerTests(ControllerTestCase):
    prefix_from = GameBorrowReturnController

    def setUp(self):
        super().setUp()
        self.add_mock_object(self.controller, 'get_borrow')
        self.add_mock_object(self.controller, 'add_flashmsg')
        self.add_mock_object(self.controller, 'redirect')
        self.borrow = self.mocks['get_borrow'].return_value

    def test_make(self):
        """GameBorrowReturnController should set status of GameBorrow to
        "returned"."""
        self.add_mock_object(self.controller, 'return_game')
        self.mocks['return_game'].return_value = True
        self.borrow.is_borrowed = True

        self.controller.make()

        self.mocks['return_game'].assert_called_once_with(self.borrow)
        self.mocks['add_flashmsg'].assert_called_once_with(
            'Gra została oddana.', 'success')
        self.mocks['redirect'].assert_called_once_with('gameborrow:list')

    def test_make_when_already_returned(self):
        """GameBorrowReturnController should do nothing if GameBorrow is
        already returned."""
        self.add_mock_object(self.controller, 'return_game')
        self.mocks['return_game'].return_value = True
        self.borrow.is_borrowed = False

        self.controller.make()

        self.assertEqual(0, self.mocks['return_game'].call_count)
        self.mocks['add_flashmsg'].assert_called_once_with(
            'Gra została oddana wcześniej.', 'warning')
        self.mocks['redirect'].assert_called_once_with('gameborrow:list')

    def test_return_game(self):
        """return_game should set is_borrowed state to False and set timestamp
        """
        self.add_mock('datetime')
        self.controller.return_game(self.borrow)

        self.assertEqual(False, self.borrow.is_borrowed)
        self.assertEqual(
            self.mocks['datetime'].utcnow.return_value,
            self.borrow.return_timestamp)
        self.db.commit.assert_called_once_with()


class SqlGameBorrowReturnControllerTests(SqlControllerTestCase):
    prefix_from = GameBorrowReturnController

    def test_get_borrow(self):
        """get_borrow should return GameBorrow with id get from
        matchdict['obj_id']"""
        self.matchdict['obj_id'] = fixtures['GameBorrow'][0].id

        entity = self.controller.get_borrow()

        self.assertEqual(fixtures['GameBorrow'][0], entity)

    def test_get_borrow_not_found(self):
        """get_borrow should raise HTTPNotFound when no GameBorrow found
        """
        self.matchdict['obj_id'] = 21321312

        self.assertRaises(HTTPNotFound, self.controller.get_borrow)


class ShowPersonHintTests(ControllerTestCase):
    prefix_from = ShowPersonHint

    def test_make(self):
        self.add_mock_object(self.controller, 'get_hint')
        self.controller.POST = {'number': 'something'}
        self.controller.data = {}

        self.controller.make()

        self.mocks['get_hint'].assert_called_once_with('something')
        obj = self.mocks['get_hint'].return_value
        self.assertEqual({
            'name': obj.name,
            'surname': obj.surname,
            'document': obj.document,
        }, self.controller.data)

    def test_get_hint_found(self):
        self.controller.document_types = ['one']
        self.add_mock_object(
            self.controller,
            'get_values_by_document_and_number')

        result = self.controller.get_hint('something')

        mocked = self.mocks['get_values_by_document_and_number']
        self.assertEqual(
            mocked.return_value,
            result)
        mocked.assert_called_once_with('one', 'something')

    def test_get_hint_not_found(self):
        self.controller.document_types = ['one']
        self.add_mock_object(
            self.controller,
            'get_values_by_document_and_number',
            side_effect=AttributeError)

        result = self.controller.get_hint('something')

        mocked = self.mocks['get_values_by_document_and_number']
        self.assertEqual(result.name, '')
        self.assertEqual(result.surname, '')
        self.assertEqual(result.document, '')
        mocked.assert_called_once_with('one', 'something')

    def test_get_values_by_document_and_number(self):
        self.add_mock('make_hash_document')
        self.add_mock_object(self.controller, 'get_game_borrow_by_stat_hash')
        self.controller.request = MagicMock()

        result = self.controller.get_values_by_document_and_number(
            'doc',
            'num')

        self.assertEqual(
            self.mocks['get_game_borrow_by_stat_hash'].return_value,
            result)

        self.assertEqual('doc', result.document)

        self.mocks['make_hash_document'].assert_called_once_with(
            self.controller.request,
            'doc',
            'num')

    def test_get_values_by_document_and_number_raise_attribute_error(self):
        self.add_mock('make_hash_document')
        self.add_mock_object(
            self.controller,
            'get_game_borrow_by_stat_hash',
            return_value=None)
        self.controller.request = MagicMock()

        self.assertRaises(
            AttributeError,
            self.controller.get_values_by_document_and_number,
            'doc',
            'num',
        )

        self.mocks['make_hash_document'].assert_called_once_with(
            self.controller.request,
            'doc',
            'num')


class SqlShowPersonHintTests(SqlControllerTestCase):
    prefix_from = ShowPersonHint

    def test_get_game_borrow_by_stat_hash(self):
        self.controller.request.registry['settings'] = main.settings
        hashed = make_hash_document(self.controller.request, 'paszport', '123')

        result = self.controller.get_game_borrow_by_stat_hash(hashed)

        self.assertEqual('FranekLast', result.name)
        self.assertEqual('KimonoLast', result.surname)
