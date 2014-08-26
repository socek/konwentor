from hatak.tests.fixtures import Fixtures as Base
from konwentor.convent.models import Convent
from konwentor.game.models import Game
from konwentor.auth.models import User
from konwentor.gamecopy.models import GameCopy, GameEntity
from konwentor.gameborrow.models import GameBorrow


class Fixtures(Base):

    def __call__(self):
        self.create_users()
        self.create_convents()
        self.create_games()
        self.create_copies()
        self.create_entities()

    def create_users(self):
        self._create(User, name='first')
        self._create(User, name='second')
        self._create(User, name='third')

    def create_convents(self):
        self._create(Convent, name='first')
        self._create(Convent, name='second')
        self._create(Convent, name='third')

    def create_games(self):
        self._create(Game, name='first')
        self._create(Game, name='second')
        self._create(Game, name='third')

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

    # def create_borrows(self):
    #     self._create_nameless(
    #         GameBorrow,
    #     )
