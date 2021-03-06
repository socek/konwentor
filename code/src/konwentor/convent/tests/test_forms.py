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
            form.fields['room'].get_name(): ['room name', ''],
        })
        form.on_success()

        mdriver.Convent.create.assert_called_once_with(name='myname')
        convent = mdriver.Convent.create.return_value
        mdriver.Room.create(name='room name', convent=convent)
        mdb.commit.assert_called_once_with()

    def test_live_submit(self, form, db, driver):
        form._parse_raw_data({
            form.fields['name'].get_name(): ['myname'],
            form.fields['room'].get_name(): ['room name'],
        })
        form.on_success()

        convent = driver.Convent.find_all().filter_by(name='myname').one()
        assert convent.rooms[0].name == 'room name'

        driver.Room.delete(convent.rooms[0])
        driver.Convent.delete(convent)
        db.flush()


class TestConventDeleteForm(LocalFixtures):

    def _get_form_class(self):
        return ConventDeleteForm

    def test_submit(self, form, Convent, mdb, mdriver):
        form._parse_raw_data({
            form.fields['obj_id'].get_name(): ['123'],
        })
        form.on_success()

        mdriver.Convent.get_by_id.assert_called_once_with(123)
        convent = mdriver.Convent.get_by_id.return_value
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
        form.model.rooms = [MagicMock(), MagicMock()]
        form._parse_raw_data({
            'name': ['myname'],
            'room': ['room0', 'room1', '']
        })

        form.on_success()

        assert form.model.name == 'myname'
        assert form.model.rooms[0].name == 'room0'
        assert form.model.rooms[1].name == 'room1'
        mdb.commit.assert_called_once_with()

    def test_on_success_when_created_new_room(self, form, mdb, mdriver):
        form.model = MagicMock()
        form.model.rooms = []
        form._parse_raw_data({
            'name': ['myname'],
            'room': ['room0']
        })

        form.on_success()

        assert form.model.name == 'myname'
        mdriver.Room.create.assert_called_once_with(
            name='room0',
            convent=form.model,
        )
        mdb.commit.assert_called_once_with()
