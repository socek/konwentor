from hatak.tests.cases import ControllerTestCase, SqlControllerTestCase
from hatak.tests.fixtures import fixtures
from pyramid.httpexceptions import HTTPNotFound

from ..controller import GameBorrowAddController, GameBorrowListController
from ..controller import GameBorrowReturnController


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
        self.form.assert_called_once_with({
            'game_entity_id': [self.data['game_entity'].id]
        })
        self.assertEqual(0, self.mocks['add_flashmsg'].call_count)
        self.assertEqual(0, self.mocks['redirect'].call_count)

    def test_make_on_form(self):
        self.form.return_value = True

        self.controller.make()

        self.assertEqual(
            self.mocks['get_game_entity'].return_value,
            self.data['game_entity'])
        self.form.assert_called_once_with({
            'game_entity_id': [self.data['game_entity'].id]
        })
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
