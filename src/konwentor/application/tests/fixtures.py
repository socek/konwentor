from haplugin.sql.fixtures import FixtureGenerator

from konwentor.convent.models import Convent
from konwentor.game.models import Game
from konwentor.gamecopy.models import GameCopy, GameEntity
from konwentor.gameborrow.models import GameBorrow
from konwentor.room.models import Room


class Fixtures(FixtureGenerator):
    users = [
        {
            'name': 'first',
            'email': 'first@gmail.com',
            'password': 'simplepass',
            'permissions': [
                ('base', 'view'),
                ('game', 'edit'),
                ('convent', 'add'),
                ('game', 'add'),
                ('gameborrow', 'add'),
                ('gamecopy', 'add'),
            ]
        },
        {
            'name': 'second',
            'email': 'second@gmail.com',
            'password': 'simplepass',
            'permissions': [('base', 'view'), ('game', 'edit')]
        },
        {
            'name': 'third',
            'email': 'third@gmail.com',
            'password': 'simplepass',
            'permissions': [('base', 'view'), ('game', 'edit')]
        },
        {
            'name': 'dynamic1',
            'email': 'dynamic1@gmail.com',
            'password': 'simplepass',
            'permissions': [('base', 'view'), ('game', 'edit')]
        },
    ]

    def make_all(self):
        self.create_users()
        self.create_convents()
        self.create_rooms()
        self.create_games()
        self.create_copies()
        self.create_entities()
        self.create_borrows()
        self.db.commit()

    def create_users(self):
        for userdata in self.users:
            self._create('Auth', **userdata)

    def create_convents(self):
        self._create(Convent, name='first')
        self._create(Convent, name='second')
        self._create(Convent, name='third')

        self._create(Convent, name='dynamic1')
        self._create(Convent, name='inactive', is_active=False)

    def create_rooms(self):
        self._create(
            Room, name='bordgames', convent=self.fixtures['Convent']['first'])
        self._create(
            Room, name='bordgames', convent=self.fixtures['Convent']['second'])
        self._create(
            Room, name='bordgames', convent=self.fixtures['Convent']['third'])

        self._create(
            Room, name='bordgames', convent=self.fixtures['Convent']['dynamic1'])
        self._create(
            Room, name='bordgames', convent=self.fixtures['Convent']['inactive'])

    def create_games(self):
        self._create(Game, name='first')
        self._create(Game, name='second')
        self._create(Game, name='third')

        self._create(Game, name='dynamic1')
        self._create(Game, name='inactive', is_active=False)

    def create_copies(self):
        self._create_nameless(
            GameCopy,
            game=self.fixtures['Game']['first'],
            owner=self.fixtures['User']['first'])

        self._create_nameless(
            GameCopy,
            game=self.fixtures['Game']['second'],
            owner=self.fixtures['User']['first'])

        self._create_nameless(
            GameCopy,
            game=self.fixtures['Game']['second'],
            owner=self.fixtures['User']['second'])

        self._create_nameless(
            GameCopy,
            game=self.fixtures['Game']['third'],
            owner=self.fixtures['User']['second'])

    def create_entities(self):
        self._create_nameless(
            GameEntity,
            gamecopy=self.fixtures['GameCopy'][0],
            convent=self.fixtures['Convent']['first'],
            count=1,
            room=self.fixtures['Convent']['first'].rooms[0],
        )

        self._create_nameless(
            GameEntity,
            gamecopy=self.fixtures['GameCopy'][1],
            convent=self.fixtures['Convent']['first'],
            count=2,
            room=self.fixtures['Convent']['first'].rooms[0],
        )

        self._create_nameless(
            GameEntity,
            gamecopy=self.fixtures['GameCopy'][2],
            convent=self.fixtures['Convent']['first'],
            count=4,
            room=self.fixtures['Convent']['first'].rooms[0],
            is_in_box=True,
        )

        self._create_nameless(
            GameEntity,
            gamecopy=self.fixtures['GameCopy'][2],
            convent=self.fixtures['Convent']['second'],
            count=4,
            room=self.fixtures['Convent']['second'].rooms[0],
        )

    def create_borrows(self):
        self._create_nameless(
            GameBorrow,
            gameentity=self.fixtures['GameEntity'][0],
            name='Franek Kimono',
            stats_hash='x',
            is_borrowed=True,
        )

        self._create_nameless(
            GameBorrow,
            gameentity=self.fixtures['GameEntity'][1],
            name='Franek Kimono',
            stats_hash='x',
            is_borrowed=True
        )

        self._create_nameless(
            GameBorrow,
            gameentity=self.fixtures['GameEntity'][0],
            name='Ten Drugi',
            stats_hash='x',
            is_borrowed=False
        )

        self._create_nameless(
            GameBorrow,
            gameentity=self.fixtures['GameEntity'][3],
            name='Franek Kimono',
            stats_hash='x',
            is_borrowed=True
        )

        self._create_nameless(
            GameBorrow,
            gameentity=self.fixtures['GameEntity'][3],
            name='FranekLast KimonoLast',
            stats_hash='x',
            is_borrowed=False
        )
