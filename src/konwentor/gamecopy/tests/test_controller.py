from hatak.tests.cases import ControllerTestCase
from hatak.tests.cases import SqlControllerTestCase
from hatak.tests.fixtures import fixtures

from ..controller import GameCopyControllerBase, GameCopyListController
from konwentor.convent.helpers import ConventWidget


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


class GameCopyListControllerTestCase(SqlControllerTestCase):
    prefix_from = GameCopyListController

    def test_get_games(self):
        """get_games should return list of games avalible on convent"""
        convent = fixtures['Convent']['first']
        result = self.controller.get_games(convent)

        self.assertEqual(3, len(result))
        for element in result:
            self.assertEqual(convent, element.GameEntity.convent)
