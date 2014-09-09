from hatak.tests.cases import ControllerTestCase
from hatak.tests.cases import SqlControllerTestCase
from hatak.tests.fixtures import fixtures

from ..controller import GameCopyAddController
from ..controller import GameCopyControllerBase, GameCopyListController
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
        form.return_value = None

        self.controller.make()

        self.mocks['add_form'].assert_called_once_with(GameCopyAddForm)
        form.assert_called_once_with(initial_data={
            'count': '1',
            'user_id': [str(self.user.id)],
            'convent_id': [str(self.session['convent_id'])]
        })
        self.assertEqual(0, self.mocks['add_flashmsg'].call_count)

    def test_form_submitted(self):
        self.session = self.controller.session = {'convent_id': 1}
        form = self.mocks['add_form'].return_value
        form.return_value = True

        self.controller.make()

        initial_data = {
            'count': '1',
            'user_id': [str(self.user.id)],
            'convent_id': [str(self.session['convent_id'])]
        }
        self.mocks['add_form'].assert_called_once_with(GameCopyAddForm)
        form.assert_called_once_with(initial_data=initial_data)
        self.assertEqual({}, form.fields)
        form._gatherFormsData.assert_called_once_with(initial_data)

        self.mocks['add_flashmsg'].assert_called_once_with(
            'Dodano grę.', 'info')

        form.get_value.assert_called_once_with('convent_id')
        self.assertEqual(
            form.get_value.return_value,
            self.session['last_convent_id'],
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
        self.add_mock_object(self.controller, 'get_convent')
        self.add_mock_object(self.controller, 'get_games')

        self.controller.make()

        self.mocks['verify_convent'].assert_called_once_with()
        self.assertEqual({
            'convent': self.mocks['get_convent'].return_value,
            'games': self.mocks['get_games'].return_value,
        }, self.data)
        self.mocks['get_games'].assert_called_once_with(
            self.mocks['get_convent'].return_value)
