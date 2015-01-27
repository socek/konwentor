from formskit.validators import NotEmpty, IsDigit
from formskit.converters import ToInt

from konwentor.application.translations import KonwentorForm
from konwentor.auth.models import User
from konwentor.convent.models import Convent
from konwentor.game.models import Game

from .models import GameCopy, GameEntity


class GameCopyAddForm(KonwentorForm):

    def create_form(self):
        field = self.add_field(
            'game_name',
            label='Gra',
            validators=[NotEmpty()])
        field.data = self.get_objects(Game, is_active=True)

        self.add_field(
            'confirmation',
            validators=[])

        field = self.add_field(
            'user_id',
            label='Właściciel',
            validators=[NotEmpty(), IsDigit()],
            convert=ToInt())
        field.data = self.get_objects(User)

        field = self.add_field(
            'convent_id',
            label='Konwent',
            validators=[NotEmpty(), IsDigit()],
            convert=ToInt())
        field.data = self.get_objects(Convent, is_active=True)

        self.add_field(
            'count',
            label='Ilość',
            validators=[NotEmpty(), IsDigit()],
            convert=ToInt())

    def get_objects(self, cls, other=False, **kwargs):
        def generator():
            yield {
                'label': '(Wybierz)',
                'value': '',
            }
            for obj in self.db.query(cls).filter_by(**kwargs).all():
                yield {
                    'label': obj.name,
                    'value': obj.id,
                }
            if other:
                yield {
                    'label': '',
                    'value': '-1',
                }
        return generator

    def on_success(self):
        data = self.get_data_dict(True)
        game = self.get_or_create_game(data['game_name'])
        user = User.get_by_id(self.db, data['user_id'])
        convent = Convent.get_by_id(self.db, data['convent_id'])

        gamecopy = self.create_gamecopy(game, user)
        gameentity = self.create_gameentity(convent, gamecopy)
        gameentity.count += data['count']

        try:
            self.db.commit()
        finally:
            self.db.rollback()

    def get_or_create_game(self, name):
        return Game.get_or_create(self.db, name=name, is_active=True)

    def create_gamecopy(self, game, user):
        gamecopy = GameCopy.get_or_create(
            self.db,
            game=game,
            owner=user)
        self.db.add(gamecopy)
        return gamecopy

    def create_gameentity(self, convent, gamecopy):
        gameentity = GameEntity.get_or_create(
            self.db,
            convent=convent,
            gamecopy=gamecopy,
        )
        self.db.add(gameentity)
        return gameentity
