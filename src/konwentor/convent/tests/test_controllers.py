from mock import MagicMock
from hatak.plugins.toster.cases import ControllerTestCase, SqlControllerTestCase
from hatak.plugins.toster.fixtures import fixtures
from pyramid.httpexceptions import HTTPNotFound

from ..controllers import ConventDelete, ChooseConventController
from ..controllers import ConventEditController
from ..controllers import ConventListController, ConventAdd
from ..controllers import EndConventController, StartConventController
from ..forms import ConventAddForm, ConventDeleteForm, ConventEditForm


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

        # -1 in len(fixtures['Convent']) means the 1 convent which is inactive
        self.assertEqual(len(fixtures['Convent']) - 1, len(convents))


class ConventAddTests(ControllerTestCase):
    prefix_from = ConventAdd

    def setUp(self):
        super().setUp()
        self.add_mock_object(self.controller, 'add_form', auto_spec=True)
        self.form = self.mocks['add_form'].return_value
        self.add_mock_object(self.controller, 'redirect', auto_spec=True)

    def test_make_success(self):
        """ConventAdd should add ConventAddForm form and redirect to
        convent:list if the form is successed"""
        self.form.return_value = True

        self.controller.make()

        self.mocks['add_form'].assert_called_once_with(ConventAddForm)
        self.mocks['redirect'].assert_called_once_with('convent:list')
        self.form.assert_called_once_with()

    def test_make_fail(self):
        """ConventAdd should add ConventAddForm form  and do nothing
        if the form is failed or not used"""
        self.form.return_value = False

        self.controller.make()

        self.mocks['add_form'].assert_called_once_with(ConventAddForm)
        self.assertFalse(self.mocks['redirect'].called)
        self.form.assert_called_once_with()


class ConventEditControllerTests(ControllerTestCase):
    prefix_from = ConventEditController

    def setUp(self):
        super().setUp()
        self.matchdict['obj_id'] = '10'
        self.add_mock_object(self.controller, 'add_form', auto_spec=True)
        self.form = self.mocks['add_form'].return_value
        self.add_mock_object(self.controller, 'redirect', auto_spec=True)
        self.add_mock_object(self.controller, 'get_convent')
        self.convent = self.mocks['get_convent'].return_value
        self.defaults = {
            'id': [self.convent.id],
            'name': [self.convent.name],
        }

    def test_make_success(self):
        """ConventEdit should add ConventEditForm form and redirect to
        convent:list if the form is successed"""
        self.form.return_value = True

        self.controller.make()

        self.form.assert_called_once_with(self.defaults)
        self.mocks['add_form'].assert_called_once_with(ConventEditForm)
        self.mocks['redirect'].assert_called_once_with('convent:list')

    def test_make_fail(self):
        """ConventEdit should add ConventAddForm form  and do nothing
        if the form is failed or not used"""
        self.form.return_value = False

        self.controller.make()

        self.form.assert_called_once_with(self.defaults)
        self.mocks['add_form'].assert_called_once_with(ConventEditForm)
        self.assertFalse(self.mocks['redirect'].called)


class SqlConventEditControllerTests(SqlControllerTestCase):
    prefix_from = ConventEditController

    def test_get_convent_when_convent_exists(self):
        convent = fixtures['Convent']['first']
        self.matchdict['obj_id'] = str(convent.id)

        result = self.controller.get_convent()

        self.assertEqual(convent, self.data['convent'])
        self.assertEqual(convent, result)

    def test_get_convent_when_convent_not_exists(self):
        self.matchdict['obj_id'] = '1231231231231124'

        self.assertRaises(HTTPNotFound, self.controller.get_convent)

    def test_get_convent_when_convent_is_inactive(self):
        convent = fixtures['Convent']['inactive']
        self.matchdict['obj_id'] = str(convent.id)

        self.assertRaises(HTTPNotFound, self.controller.get_convent)


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

    def test_verify_convent_id_on_not_active_convent(self):
        """verify_convent_id should raise HTTPNotFound when inpute id of not
        active convent."""
        self.controller.matchdict = {
            'obj_id': fixtures['Convent']['inactive'].id,
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
