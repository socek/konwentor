from haplugin.sql.fixtures import FixtureGenerator

from konwentor.convent.models import Convent
from konwentor.game.models import Game
from konwentor.gamecopy.models import GameCopy, GameEntity
from konwentor.gameborrow.models import GameBorrow
from konwentor.auth.models import User


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
        self.create_games()
        self.create_copies()
        self.create_entities()
        self.create_borrows()

    def create_users(self):
        for userdata in self.users:
            password = userdata.pop('password')
            permissions = userdata.pop('permissions')
            user = self._create(User, **userdata)
            user.set_password(password)
            for perm in permissions:
                user.add_permission(self.db, *perm)

    def create_convents(self):
        self._create(Convent, name='first')
        self._create(Convent, name='second')
        self._create(Convent, name='third')

        self._create(Convent, name='dynamic1')
        self._create(Convent, name='inactive', is_active=False)

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
        )

        self._create_nameless(
            GameEntity,
            gamecopy=self.fixtures['GameCopy'][1],
            convent=self.fixtures['Convent']['first'],
            count=2,
        )

        self._create_nameless(
            GameEntity,
            gamecopy=self.fixtures['GameCopy'][2],
            convent=self.fixtures['Convent']['first'],
            count=4,
        )

        self._create_nameless(
            GameEntity,
            gamecopy=self.fixtures['GameCopy'][2],
            convent=self.fixtures['Convent']['second'],
            count=4,
        )

    def create_borrows(self):
        obj = self._create_nameless(
            GameBorrow,
            gameentity=self.fixtures['GameEntity'][0],
            name='Franek',
            surname='Kimono',
            stats_hash='x',
            is_borrowed=True,
        )
        obj.settings = self.application.settings
        obj.set_document('paszport', '123')

        obj = self._create_nameless(
            GameBorrow,
            gameentity=self.fixtures['GameEntity'][1],
            name='Franek',
            surname='Kimono',
            stats_hash='x',
            is_borrowed=True
        )
        obj.settings = self.application.settings
        obj.set_document('paszport', '123')

        obj = self._create_nameless(
            GameBorrow,
            gameentity=self.fixtures['GameEntity'][0],
            name='Ten',
            surname='Drugi',
            stats_hash='x',
            is_borrowed=False
        )
        obj.settings = self.application.settings
        obj.set_document('paszport', '1234')

        obj = self._create_nameless(
            GameBorrow,
            gameentity=self.fixtures['GameEntity'][3],
            name='Franek',
            surname='Kimono',
            stats_hash='x',
            is_borrowed=True
        )
        obj.settings = self.application.settings
        obj.set_document('paszport', '123')

        obj = self._create_nameless(
            GameBorrow,
            gameentity=self.fixtures['GameEntity'][3],
            name='FranekLast',
            surname='KimonoLast',
            stats_hash='x',
            is_borrowed=False
        )
        obj.settings = self.application.settings
        obj.set_document('paszport', '123')
