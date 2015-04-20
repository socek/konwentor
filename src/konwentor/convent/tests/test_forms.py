from pytest import yield_fixture
from mock import MagicMock, patch

from konwentor.convent.forms import ConventAddForm, ConventDeleteForm
from konwentor.convent.forms import ConventEditForm
from konwentor.application.testing import FormFixture


class LocalFixtures(FormFixture):

    @yield_fixture
    def Convent(self):
        patcher = patch('konwentor.convent.forms.Convent')
        with patcher as mock:
            yield mock

    @yield_fixture
    def get_value(self, form, fixtures):
        convent_id = fixtures['Convent']['first'].id
        patcher = patch.object(form, 'get_value', return_value=str(convent_id))
        with patcher as mock:
            yield mock


class TestConventAddForm(LocalFixtures):

    def _get_form_class(self):
        return ConventAddForm

    def test_submit(self, form, Convent, mdb, mdriver):
        form._parse_raw_data({
            form.fields['name'].get_name(): ['myname'],
        })
        form.on_success()

        mdriver.Convent.create.assert_called_once_with(name='myname')
        mdb.flush.assert_called_once_with()


class TestConventDeleteForm(LocalFixtures):

    def _get_form_class(self):
        return ConventDeleteForm

    def test_submit(self, form, Convent, mdb):
        form._parse_raw_data({
            form.fields['obj_id'].get_name(): ['123'],
        })
        form.on_success()

        Convent.get_by_id.assert_called_once_with(
            mdb, 123)
        convent = Convent.get_by_id.return_value
        assert convent.is_active is False
        mdb.commit.assert_called_once_with()


class TestConventEditForm(LocalFixtures):

    def _get_form_class(self):
        return ConventEditForm

    def test_id_exists_validator_success(self, form, get_value, fixtures):
        form.form_validators[0].validate()

        get_value.assert_called_once_with('id')
        assert fixtures['Convent']['first'], form.model

    def test_id_exists_validator_fail(self, form, fixtures):
        form._parse_raw_data({'id': ['1239032']})
        assert form.form_validators[0].validate() is False

    def test_submit(self, form, mdb):
        form.model = MagicMock()
        form._parse_raw_data({'name': ['myname']})

        form.on_success()

        assert form.model.name == 'myname'
        mdb.commit.assert_called_once_with()
