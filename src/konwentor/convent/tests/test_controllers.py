from mock import MagicMock
from hatak.tests.cases import ControllerTestCase, SqlControllerTestCase
from hatak.tests.fixtures import fixtures
from pyramid.httpexceptions import HTTPNotFound

from ..forms import ConventAddForm, ConventDeleteForm
from konwentor.convent.controllers import ConventDelete
from konwentor.convent.controllers import ChooseConventController
from konwentor.convent.controllers import ConventListController, ConventAdd
from konwentor.convent.controllers import EndConventController
from konwentor.convent.controllers import StartConventController


class ConventListControllerTests(ControllerTestCase):
    prefix_from = ConventListController

    def test_make(self):
        """ConventListController should create convents widgets and get actual
        selected convent_id from session"""
        self.add_mock_object(
            self.controller, 'get_convent_widgets', auto_spec=True)
        self.controller.session = {
            'convent_id': 10,
        }
        self.controller.data = {}

        self.controller.make()

        self.assertEqual(
            {
                'choosed_id': 10,
                'convents': self.mocks['get_convent_widgets'].return_value,
            },
            self.controller.data)

    def test_get_convent_widgets(self):
        """get_convent_widgets should wrap all convents with ConventWidget"""
        self.add_mock('ConventWidget')
        self.add_mock_object(self.controller, 'get_convents')
        self.mocks['get_convents'].return_value = ['1', ]

        result = self.controller.get_convent_widgets()

        self.assertEqual(
            [self.mocks['ConventWidget'].return_value],
            result)

        self.mocks['ConventWidget'].assert_called_once_with(
            self.request, '1')


class ConventListControllerSqlTests(SqlControllerTestCase):
    prefix_from = ConventListController

    def test_get_convents(self):
        """get_convents should return all convents"""
        convents = self.controller.get_convents()
        for convent in convents:
            self.assertTrue(convent in fixtures['Convent'].values())

        self.assertEqual(len(fixtures['Convent']), len(convents))


class ConventAddTests(ControllerTestCase):
    prefix_from = ConventAdd

    def test_make_success(self):
        """ConventAdd should add ConventAddForm form and redirect to
        convent:list if the form is successed"""
        self.add_mock_object(self.controller, 'add_form', auto_spec=True)
        form = self.mocks['add_form'].return_value
        form.return_value = True
        self.add_mock_object(self.controller, 'redirect', auto_spec=True)

        self.controller.make()

        self.mocks['add_form'].assert_called_once_with(ConventAddForm)
        self.mocks['redirect'].assert_called_once_with('convent:list')

    def test_make_fail(self):
        """ConventAdd should add ConventAddForm form  and do nothing
        if the form is failed or not used"""
        self.add_mock_object(self.controller, 'add_form', auto_spec=True)
        form = self.mocks['add_form'].return_value
        form.return_value = False

        self.controller.make()

        self.mocks['add_form'].assert_called_once_with(ConventAddForm)


class ConventDeleteTests(ControllerTestCase):
    prefix_from = ConventDelete

    def test_make_success(self):
        """make should verify convent_id, proccess form and redirect if form
        was successed."""
        self.add_mock_object(
            self.controller,
            'verify_convent_id',
            auto_spec=True)
        self.add_mock_object(
            self.controller,
            'add_form',
            auto_spec=True)
        self.add_mock_object(
            self.controller,
            'redirect',
            auto_spec=True)
        self.controller.matchdict = {
            'obj_id': 'my obj id',
        }
        form = self.mocks['add_form'].return_value
        form.return_value = True

        self.controller.make()

        self.mocks['verify_convent_id'].assert_called_once_with()
        self.mocks['add_form'].assert_called_once_with(ConventDeleteForm)
        form.assert_called_once_with({
            'obj_id': 'my obj id',
        })
        self.mocks['redirect'].assert_called_once_with('convent:list')

    def test_make_fail(self):
        """make should verify convent_id, and proccess form"""
        self.add_mock_object(
            self.controller,
            'verify_convent_id',
            auto_spec=True)
        self.add_mock_object(
            self.controller,
            'add_form',
            auto_spec=True)
        self.add_mock_object(
            self.controller,
            'redirect',
            auto_spec=True)
        self.controller.matchdict = {
            'obj_id': 'my obj id',
        }
        form = self.mocks['add_form'].return_value
        form.return_value = False

        self.controller.make()

        self.mocks['verify_convent_id'].assert_called_once_with()
        self.mocks['add_form'].assert_called_once_with(ConventDeleteForm)
        form.assert_called_once_with({
            'obj_id': 'my obj id',
        })


class SqlConventDeleteTests(SqlControllerTestCase):
    prefix_from = ConventDelete

    def test_verify_convent_id_success(self):
        """verify_convent_id should place Convent object in .data['convent']
        when the convent_id is poiting to existing row in db."""
        self.controller.data = {}
        self.controller.matchdict = {
            'obj_id': fixtures['Convent']['first'].id,
        }

        self.controller.verify_convent_id()

        self.assertEqual(
            fixtures['Convent']['first'],
            self.controller.data['convent'],
        )

    def test_verify_convent_id_failed(self):
        """verify_convent_id should raise HTTPNotFound when no convent found"""
        self.controller.matchdict = {
            'obj_id': 12331,
        }

        self.assertRaises(
            HTTPNotFound,
            self.controller.verify_convent_id,
        )


class ChooseConventControllerTests(ControllerTestCase):
    prefix_from = ChooseConventController

    def test_make(self):
        """ChooseConventController should verify convent_id, switch selected
        convent and redirect to gamecopy:list"""
        self.add_mock_object(self.controller, 'verify_convent_id')
        self.add_mock_object(self.controller, 'redirect')
        self.controller.matchdict = {
            'obj_id': '10',
        }
        self.controller.session = {}

        self.controller.make()

        self.mocks['verify_convent_id'].assert_called_once_with()
        self.mocks['redirect'].assert_called_once_with('gamecopy:list')
        self.assertEqual(
            10,
            self.controller.session['convent_id'],
        )


class StartConventControllerTests(ControllerTestCase):
    prefix_from = StartConventController

    def test_make(self):
        """StartConventController should verify convent_id, switch_convent,
        start it and redirect to gamecopy:add"""
        self.add_mock_object(self.controller, 'verify_convent_id')
        self.add_mock_object(self.controller, 'switch_convent')
        self.add_mock_object(self.controller, 'redirect')
        self.data['convent'] = MagicMock()

        self.controller.make()

        self.mocks['verify_convent_id'].assert_called_once_with()
        self.mocks['switch_convent'].assert_called_once_with()
        self.assertEqual('running', self.data['convent'].state)
        self.db.commit.assert_called_once_with()
        self.mocks['redirect'].assert_called_once_with('gamecopy:add')


class EndConventControllerTests(ControllerTestCase):
    prefix_from = EndConventController

    def test_make(self):
        """EndConventController should verify convent_id, end convent,
        and redirect to convent:list"""
        self.add_mock_object(self.controller, 'verify_convent_id')
        self.add_mock_object(self.controller, 'redirect')
        self.data['convent'] = MagicMock()

        self.controller.make()

        self.mocks['verify_convent_id'].assert_called_once_with()
        self.assertEqual('ended', self.data['convent'].state)
        self.db.commit.assert_called_once_with()
        self.mocks['redirect'].assert_called_once_with('convent:list')


class ConventDatabaseTest(ControllerTestCase):

    prefix_from = ConventListController

    def test_all(self):
        self.add_mock('Convent')
        result = self.controller.get_convents()
        self.assertEqual(
            self.mocks['Convent'].get_all.return_value,
            result)
        self.mocks['Convent'].get_all.assert_called_once_with(self.db)
