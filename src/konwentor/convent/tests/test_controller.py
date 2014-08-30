from hatak.tests.cases import ControllerTestCase, SqlControllerTestCase
from hatak.tests.fixtures import fixtures

from konwentor.convent.controller import ConventListController, ConventAdd
from ..forms import ConventAddForm


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


class ConventAdd(ControllerTestCase):
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
