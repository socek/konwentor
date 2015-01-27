from haplugin.toster import FormTestCase, SqlFormTestCase
from haplugin.toster.fixtures import fixtures
from mock import MagicMock

from konwentor.convent.forms import ConventAddForm, ConventDeleteForm
from konwentor.convent.forms import ConventEditForm


class ConventAddFormTest(FormTestCase):

    prefix_from = ConventAddForm

    def test_submit(self):
        self.add_mock('Convent')
        self.form._parse_raw_data({
            self.form.fields['name'].get_name(): ['myname'],
        })
        self.form.on_success()

        self.mocks['Convent'].create.assert_called_once_with(
            self.db, name='myname')


class ConventDeleteFormTest(FormTestCase):

    prefix_from = ConventDeleteForm

    def test_submit(self):
        self.add_mock('Convent')
        self.form._parse_raw_data({
            self.form.fields['obj_id'].get_name(): ['123'],
        })
        self.form.on_success()

        self.mocks['Convent'].get_by_id.assert_called_once_with(
            self.db, 123)
        convent = self.mocks['Convent'].get_by_id.return_value
        self.assertEqual(False, convent.is_active)
        self.db.commit.assert_called_once_with()


class SqlConventEditFormTest(SqlFormTestCase):

    prefix_from = ConventEditForm

    def test_id_exists_validator_success(self):
        convent_id = fixtures['Convent']['first'].id
        self.add_mock_object(
            self.form, 'get_value', return_value=str(convent_id))
        self.form.form_validators[0].validate()

        self.mocks['get_value'].assert_called_once_with('id')
        self.assertEqual(fixtures['Convent']['first'], self.form.model)

    def test_id_exists_validator_fail(self):
        self.add_mock_object(
            self.form, 'get_value', return_value='1234566')
        self.assertEqual(False, self.form.form_validators[0].validate())


class ConventEditFormTest(FormTestCase):
    prefix_from = ConventEditForm

    def test_submit(self):
        self.add_mock_object(
            self.form, 'get_value', return_value='myname')

        self.form.model = MagicMock()
        self.form._parse_raw_data({})

        self.form.on_success()

        self.assertEqual('myname', self.form.model.name)
        self.db.commit.assert_called_once_with()
