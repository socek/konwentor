from pytest import yield_fixture, mark
from mock import MagicMock, create_autospec, patch

from ..forms import GameCopyAddForm
from ..models import GameCopy, GameEntity
from konwentor.auth.models import User
from konwentor.convent.models import Convent
from konwentor.game.models import Game
from konwentor.application.testing import FormFixture
from konwentor.room.models import Room


class TestGameCopyAddForm(FormFixture):

    def _get_form_class(self):
        return GameCopyAddForm

    @yield_fixture
    def create_gamecopy(self, form):
        with patch.object(form, 'create_gamecopy', autospec=True) as mock:
            yield mock

    @yield_fixture
    def create_gameentity(self, form):
        with patch.object(form, 'create_gameentity', autospec=True) as mock:
            yield mock

    def test_get_objects(self, form, mdriver):
        """get_objects should return list of dicts"""
        mdriver.self.find_by.call_count = 0
        example_model = MagicMock()
        mdriver.self.find_by.return_value.all.return_value = [
            example_model
        ]

        data = list(form.get_objects('self')())

        assert data[0] == {
            'label': '(Wybierz)',
            'value': '',
        }

        assert data[1] == {
            'label': example_model.name,
            'value': example_model.id,
        }

        mdriver.self.find_by.assert_called_with()

    def test_get_objects_with_other(self, form, mdriver):
        """get_objects should return list of dicts"""
        mdriver.self.find_by.call_count = 0
        example_model = MagicMock()
        mdriver.self.find_by.return_value.all.return_value = [
            example_model
        ]

        data = list(form.get_objects('self', True, something=True)())

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

        mdriver.self.find_by.assert_called_with(something=True)

    def test_submit(
        self,
        form,
        query,
        create_gamecopy,
        create_gameentity,
        mdb,
        mdriver,
    ):
        """Submit should create gamecopy and gameentity (with count)."""
        create_gameentity.return_value.count = 3

        form.parse_dict({
            'game_name': '1',
            'user_id': 4,
            'room_id': 5,
            'count': 2,
        })
        form.on_success()

        mdriver.Game.upsert.assert_called_once_with(
            name='1', is_active=True)
        mdriver.User.get_by_id.assert_called_once_with(4)
        mdriver.Room.get_by_id.assert_called_once_with(5)

        create_gamecopy.assert_called_once_with(
            mdriver.Game.upsert.return_value,
            mdriver.User.get_by_id.return_value,
        )

        create_gameentity.assert_called_once_with(
            mdriver.Room.get_by_id.return_value,
            create_gamecopy.return_value,
        )
        gameentity = create_gameentity.return_value

        assert gameentity.count == 5

        mdb.commit.assert_called_once_with()
        mdb.rollback.assert_called_once_with()

    def test_create_gamecopy(self, form, mdb, mdriver):
        """create_gamecopy should get or create GameCopy object."""
        game = create_autospec(Game())
        user = create_autospec(User())

        result = form.create_gamecopy(game, user)
        assert result == mdriver.GameCopy.upsert.return_value
        mdriver.GameCopy.upsert.assert_called_once_with(
            game=game,
            owner=user)

    def test_create_gameentity(self, form, mdriver):
        """create_gameentity should create GameEntity."""
        room = create_autospec(Room())
        gamecopy = create_autospec(GameCopy())

        gameentity = form.create_gameentity(room, gamecopy)
        assert gameentity == mdriver.GameEntity.upsert.return_value
        mdriver.GameEntity.upsert.assert_called_once_with(
            convent=room.convent,
            gamecopy=gamecopy,
            room=room,
        )

    def test_upsert_game(self, form, mdb, mdriver):
        """
        upsert_game should get game from mdb or create it if not found
        """
        result = form.upsert_game('myname')

        game = mdriver.Game.upsert.return_value
        assert result == game
        mdriver.Game.upsert.assert_called_once_with(
            name='myname', is_active=True)

    @mark.usefixtures('CsrfMustMatch')
    def test_success(self, form, fixtures, postdata, db, query):
        """GameCopyAddForm is creating data."""
        game = fixtures['Game']['dynamic1']
        user = fixtures['User']['dynamic1']
        room = fixtures['Convent']['dynamic1'].rooms[0]

        postdata[form.fields['game_name'].get_name()] = [game.name, ]
        postdata[form.fields['user_id'].get_name()] = [str(user.id), ]
        postdata[form.fields['room_id'].get_name()] = [str(room.id), ]
        postdata[form.fields['count'].get_name()] = ['5', ]

        form.validate()
        db.flush()

        entity = (
            query(GameEntity)
            .filter(GameEntity.room == room)
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
