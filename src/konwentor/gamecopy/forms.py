from formskit import Field

from konwentor.application.forms import PostForm
from konwentor.forms.validators import NotEmpty, IsDigit
from konwentor.auth.models import User
from konwentor.convent.models import Convent
from konwentor.game.models import Game

from .models import GameCopy, GameCopyOnConvent


class GameCopyAddForm(PostForm):

    def createForm(self):
        field = Field(
            'game_id',
            label='Gra',
            validators=[NotEmpty(), IsDigit()])
        field.data = self.get_objects(Game)
        self.addField(field)

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
        field.data = self.get_objects(Convent)
        self.addField(field)

        field = Field(
            'count',
            label='Ilość',
            validators=[NotEmpty(), IsDigit()])
        self.addField(field)

    def get_objects(self, cls):
        objects = [{
            'label': '(Wybierz)',
            'value': '',
        }]
        for obj in self.db.query(cls).all():
            objects.append({
                'label': obj.name,
                'value': str(obj.id),
            })
        return objects

    def get_object(self, cls, _id):
        return self.db.query(cls).filter_by(id=_id).one()

    def submit(self, data):
        game = self.get_object(Game, data['game_id'][0])
        user = self.get_object(User, data['user_id'][0])
        convent = self.get_object(Convent, data['convent_id'][0])
        count = data['count'][0]

        gamecopy = self.create_gamecopy(game, user)
        gameonconvent = self.create_gameonconvent(convent, gamecopy)
        gameonconvent.count += int(count)

        self.db.add(gameonconvent)
        try:
            self.db.commit()
        finally:
            self.db.rollback()

    def create_gamecopy(self, game, user):
        gamecopy = GameCopy.get_or_create(
            self.db,
            game=game,
            owner=user)
        self.db.add(gamecopy)
        return gamecopy

    def create_gameonconvent(self, convent, gamecopy):
        if gamecopy.id is None:
            gameonconvent = GameCopyOnConvent(
                convent=convent,
            )
            gameonconvent.gamecopy = gamecopy
        else:
            gameonconvent = GameCopyOnConvent.get_or_create(
                self.db,
                convent=convent,
                gamecopy=gamecopy,
            )
        self.db.add(gameonconvent)
        return gameonconvent