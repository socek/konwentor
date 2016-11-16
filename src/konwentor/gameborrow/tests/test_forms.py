from mock import patch, MagicMock, call
from pytest import yield_fixture, fixture
from sqlalchemy.orm.exc import NoResultFound

from ..forms import GameBorrowAddForm, GameBorrowReturnForm
from ..forms import IsGameBorrowExisting
from konwentor.application.testing import FormFixture


class LocalFixtures(FormFixture):

    @yield_fixture
    def GameBorrow(self):
        patcher = patch('konwentor.gameborrow.forms.GameBorrow')
        with patcher as mock:
            yield mock


class TestGameBorrowAddForm(LocalFixtures):

    def _get_form_class(self):
        return GameBorrowAddForm

    @yield_fixture
    def get_entity(self, form):
        with patch.object(form, 'get_entity') as mock:
            yield mock

    @fixture
    def entity(self, get_entity):
        return get_entity.return_value

    def test_get_avalible_documents(self, form):
        elements = form.get_avalible_documents()
        assert elements[0] == {
            'label': 'Inne',
            'value': 'inne',
        }

    def test_overal_validation(self, form, entity, get_entity):
        """overalValidation should return GameEntity.is_avalible"""
        entity.is_avalible.return_value = True

        assert form.overal_validation({'game_entity_id': ['1']}) is True
        get_entity.assert_called_once_with('1')

    def test_overal_validation_false(self, form, entity, get_entity):
        """overalValidation should return GameEntity.is_avalible"""
        entity.is_avalible.return_value = False

        assert form.overal_validation({'game_entity_id': ['1']}) is False

        get_entity.assert_called_once_with('1')
        assert form.message == 'Ta gra nie ma już wolnych kopii.'

    def test_submit(self, form, GameBorrow, mdb):
        form.parse_dict({
            'game_entity_id': [12],
            'name': ['sds'],
            'document': ['inne'],
        })
        form.on_success()

        element = GameBorrow.return_value

        assert element.game_entity_id == 12
        assert element.name == 'sds'
        assert element.document == 'inne'
        assert element.is_borrowed is True

        mdb.add.assert_called_once_with(element)
        mdb.commit.assert_called_once_with()

    def test_get_entity(self, form, fixtures):
        _id = fixtures['GameEntity'][0].id
        entity = form.get_entity(_id)

        assert entity == fixtures['GameEntity'][0]


class TestGameBorrowReturnForm(LocalFixtures):

    def _get_form_class(self):
        return GameBorrowReturnForm

    def test_get_avalible_games(self, form, fixtures):
        form.set_value('room_id', fixtures['Convent']['first'].rooms[0].id)

        result = list(form.get_avalible_games())

        assert len(result) == 2
        assert result[0].GameEntity.id == 2
        assert result[1].GameEntity.id == 3

    @yield_fixture
    def get_avalible_games(self, form, obj):
        patcher = patch.object(form, 'get_avalible_games')
        with patcher as mock:
            mock.return_value = [obj]
            yield mock

    @yield_fixture
    def return_game(self, form):
        patcher = patch.object(form, 'return_game')
        with patcher as mock:
            yield mock

    @yield_fixture
    def borrow_next(self, form):
        patcher = patch.object(form, 'borrow_next')
        with patcher as mock:
            yield mock

    @yield_fixture
    def get_value(self, form):
        patcher = patch.object(form, 'get_value')
        with patcher as mock:
            yield mock

    @yield_fixture
    def datetime(self):
        patcher = patch('konwentor.gameborrow.forms.datetime')
        with patcher as mock:
            yield mock

    @fixture
    def obj(self):
        obj = MagicMock()
        obj.name = 'name'
        obj.User.name = 'owner'
        return obj

    def test_get_entity_ids(self, obj, form, get_avalible_games):
        data = list(form.get_entity_ids())
        assert data[0].value == ''
        assert data[0].label == '(nie wypożycza)'
        assert data[1].value == obj.GameEntity.id
        assert data[1].label == 'owner - name'

    def test_submit(self, form, return_game, borrow_next):
        form.on_success()

        return_game.assert_called_once_with()
        borrow_next.assert_called_once_with()
        form.db.flush.assert_called_once_with()
        form.db.commit.assert_called_once_with()

    def test_return_game(
        self,
        form,
        datetime
    ):
        form.borrow = MagicMock()

        form.return_game()

        assert form.borrow.is_borrowed is False
        assert form.borrow.return_timestamp == datetime.utcnow.return_value

    def test_borrow_next_whit_empty_game_entity_id(self, form, get_value):
        get_value.return_value = None

        form.borrow_next()

        get_value.assert_called_once_with('game_entity_id')

    def test_borrow_next(self, form, get_value, GameBorrow, datetime):
        borrow = form.borrow = MagicMock()
        get_value.return_value = 123

        form.borrow_next()

        get_value.assert_has_calls([
            call('game_entity_id'),
            call('game_entity_id'),
        ])
        GameBorrow.assert_called_once_with()
        obj = GameBorrow.return_value
        assert obj == form.new_borrow

        obj.assign_request.assert_called_once_with(self.request)
        assert obj.game_entity_id == 123
        assert borrow.name == obj.name
        assert obj.surname == borrow.surname
        assert obj.stats_hash == borrow.stats_hash
        assert obj.is_borrowed is True
        assert obj.borrowed_timestamp == datetime.utcnow.return_value
        form.db.add.assert_called_once_with(obj)


class TestIsGameBorrowExisting(LocalFixtures):

    def _get_form_class(self):
        return MagicMock()

    @fixture
    def validator(self, form):
        obj = IsGameBorrowExisting()
        obj.set_form(form)
        return obj

    @yield_fixture
    def get_borrow(self, validator):
        patcher = patch.object(validator, 'get_borrow')
        with patcher as mock:
            yield mock

    def test_validate_fail(self, get_borrow, validator, form):
        get_borrow.side_effect = NoResultFound

        assert validator.validate() is False
        form.get_value.assert_called_once_with('game_borrow_id')
        get_borrow.assert_called_once_with(form.get_value.return_value)

    def test_validate_success(self, get_borrow, validator, form):
        assert validator.validate() is True
        form.get_value.assert_called_once_with('game_borrow_id')
        get_borrow.assert_called_once_with(
            form.get_value.return_value)
        assert form.borrow == get_borrow.return_value

    def test_get_borrow(self, validator, fixtures, form, request):
        form.driver = request.driver
        borrow = validator.get_borrow(fixtures['GameBorrow'][0].id)

        assert borrow == fixtures['GameBorrow'][0]
