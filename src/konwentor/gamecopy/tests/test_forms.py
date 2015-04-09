from pytest import yield_fixture
from mock import MagicMock, create_autospec, patch

from ..forms import GameCopyAddForm
from ..models import GameCopy, GameEntity
from konwentor.auth.models import User
from konwentor.convent.models import Convent
from konwentor.game.models import Game
from konwentor.application.testing import FormFixture


class TestGameCopyAddForm(FormFixture):

    def _get_form_class(self):
        return GameCopyAddForm

    @yield_fixture
    def Game(self):
        with patch('konwentor.gamecopy.forms.Game') as mock:
            yield mock

    @yield_fixture
    def User(self):
        with patch('konwentor.gamecopy.forms.User') as mock:
            yield mock

    @yield_fixture
    def Convent(self):
        with patch('konwentor.gamecopy.forms.Convent') as mock:
            yield mock

    @yield_fixture
    def GameCopy(self):
        with patch('konwentor.gamecopy.forms.GameCopy') as mock:
            yield mock

    @yield_fixture
    def GameEntity(self):
        with patch('konwentor.gamecopy.forms.GameEntity') as mock:
            yield mock

    @yield_fixture
    def create_gamecopy(self, form):
        with patch.object(form, 'create_gamecopy', autospec=True) as mock:
            yield mock

    @yield_fixture
    def create_gameentity(self, form):
        with patch.object(form, 'create_gameentity', autospec=True) as mock:
            yield mock

    def test_get_objects(self, form, query):
        """get_objects should return list of dicts"""
        query.return_value.filter_by.call_count = 0
        example_model = MagicMock()
        query.return_value.filter_by.return_value.all.return_value = [
            example_model
        ]

        data = list(form.get_objects(self)())

        assert data[0] == {
            'label': '(Wybierz)',
            'value': '',
        }

        assert data[1] == {
            'label': example_model.name,
            'value': example_model.id,
        }

        query.assert_called_with(self)
        query.return_value.filter_by.assert_called_once_with()
        query.return_value.filter_by.return_value.all.assert_called_with()

    def test_get_objects_with_other(self, form, query):
        """get_objects should return list of dicts"""
        query.return_value.filter_by.call_count = 0
        example_model = MagicMock()
        query.return_value.filter_by.return_value.all.return_value = [
            example_model]

        data = list(form.get_objects(self, True)())

        assert data[0] == {
            'label': '(Wybierz)',
            'value': '',
        }

        assert data[1] == {
            'label': example_model.name,
            'value': example_model.id,
        }

        assert data[2] == {
            'label': '',
            'value': '-1',
        }

        query.assert_called_with(self)
        query.return_value.filter_by.assert_called_once_with()
        query.return_value.filter_by.return_value.all.assert_called_with()

    def test_submit(
        self,
        form,
        query,
        Game,
        User,
        Convent,
        create_gamecopy,
        create_gameentity,
        mdb,
    ):
        """Submit should create gamecopy and gameentity (with count)."""
        create_gameentity.return_value.count = 3

        form.parse_dict({
            'game_name': '1',
            'user_id': 4,
            'convent_id': 5,
            'count': 2,
        })
        form.on_success()

        Game.get_or_create.assert_called_once_with(
            mdb, name='1', is_active=True)
        User.get_by_id.assert_called_once_with(mdb, 4)
        Convent.get_by_id.assert_called_once_with(mdb, 5)

        create_gamecopy.assert_called_once_with(
            Game.get_or_create.return_value,
            User.get_by_id.return_value,
        )

        create_gameentity.assert_called_once_with(
            Convent.get_by_id.return_value,
            create_gamecopy.return_value,
        )
        gameentity = create_gameentity.return_value

        assert gameentity.count == 5

        mdb.commit.assert_called_once_with()
        mdb.rollback.assert_called_once_with()

    def test_create_gamecopy(self, form, GameCopy, mdb):
        """create_gamecopy should get or create GameCopy object."""
        game = create_autospec(Game())
        user = create_autospec(User())

        result = form.create_gamecopy(game, user)
        assert result == GameCopy.get_or_create.return_value
        GameCopy.get_or_create.assert_called_once_with(
            mdb,
            game=game,
            owner=user)
        mdb.add.assert_called_once_with(result)

    def test_create_gameentity(self, form, mdb, GameEntity):
        """create_gameentity should create GameEntity."""
        convent = create_autospec(Convent())
        gamecopy = create_autospec(GameCopy())

        gameentity = form.create_gameentity(convent, gamecopy)
        assert gameentity == GameEntity.get_or_create.return_value
        GameEntity.get_or_create.assert_called_once_with(
            mdb,
            convent=convent,
            gamecopy=gamecopy)
        mdb.add.assert_called_once_with(gameentity)

    def test_get_or_create_game(self, form, Game, mdb):
        """
        get_or_create_game should get game from mdb or create it if not found
        """
        result = form.get_or_create_game('myname')

        game = Game.get_or_create.return_value
        assert result == game
        Game.get_or_create.assert_called_once_with(
            mdb, name='myname', is_active=True)

    def test_success(self, form, fixtures, postdata, db, query):
        """GameCopyAddForm is creating data."""
        game = fixtures['Game']['dynamic1']
        user = fixtures['User']['dynamic1']
        convent = fixtures['Convent']['dynamic1']

        postdata[form.fields['game_name'].get_name()] = [game.name, ]
        postdata[form.fields['user_id'].get_name()] = [str(user.id), ]
        postdata[form.fields['convent_id'].get_name()] = [str(convent.id), ]
        postdata[form.fields['count'].get_name()] = ['5', ]

        form.validate()
        db.flush()

        entity = (
            query(GameEntity)
            .filter(GameEntity.convent == convent)
            .one()
        )
        copy = entity.gamecopy

        assert entity.count == 5
        assert copy.game == game
        assert copy.owner == user

        try:
            db.delete(copy)
            db.delete(entity)
            db.commit()
        finally:
            db.rollback()
