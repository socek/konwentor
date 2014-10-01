from formskit import Field

from haplugin.formskit import PostForm
from konwentor.forms.validators import NotEmpty, IsDigit
from konwentor.auth.models import User
from konwentor.convent.models import Convent
from konwentor.game.models import Game

from .models import GameCopy, GameEntity


class GameCopyAddForm(PostForm):

    def createForm(self):
        field = Field(
            'game_name',
            label='Gra',
            validators=[NotEmpty()])
        field.data = self.get_objects(Game, is_active=True)
        self.addField(field)

        self.addField(Field(
            'confirmation',
            validators=[]))

        field = Field(
            'user_id',
            label='Właściciel',
            validators=[NotEmpty(), IsDigit()])
        field.data = self.get_objects(User)
        self.addField(field)

        field = Field(
            'convent_id',
            label='Konwent',
            validators=[NotEmpty(), IsDigit()])
        field.data = self.get_objects(Convent, is_active=True)
        self.addField(field)

        field = Field(
            'count',
            label='Ilość',
            validators=[NotEmpty(), IsDigit()])
        self.addField(field)

    def get_objects(self, cls, other=False, **kwargs):
        objects = [{
            'label': '(Wybierz)',
            'value': '',
        }]
        for obj in self.db.query(cls).filter_by(**kwargs).all():
            objects.append({
                'label': obj.name,
                'value': str(obj.id),
            })
        if other:
            objects.append({
                'label': '',
                'value': '-1',
            })
        return objects

    def submit(self, data):
        game = self.get_or_create_game(data['game_name'][0])
        user = User.get_by_id(self.db, data['user_id'][0])
        convent = Convent.get_by_id(self.db, data['convent_id'][0])
        count = data['count'][0]

        gamecopy = self.create_gamecopy(game, user)
        gameentity = self.create_gameentity(convent, gamecopy)
        gameentity.count += int(count)

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
