from sqlalchemy import func, desc, distinct

from konwentor.application.driver import KonwentorDriver

from .models import Game
from konwentor.gamecopy.models import GameEntity, GameCopy
from konwentor.gameborrow.models import GameBorrow
from konwentor.auth.models import User


class GameDriver(KonwentorDriver):
    name = 'Game'
    model = Game

    def get_actives(self):
        return self.get_all().filter_by(is_active=True)

    def get_active(self, obj_id):
        return (
            self.query(self.model)
            .filter_by(id=obj_id, is_active=True)
            .one()
        )

    def get_by_name(self, name):
        return self.query(self.model).filter_by(name=name).one()

    def get_game_list_view(self, convent):
        return (
            self.query(
                GameEntity,
                Game,
                Game.name,
                User.name.label('author_name'))
            .join(GameCopy).join(Game).join(User)
            .filter(
                GameEntity.convent_id == convent.id,
                Game.is_active.is_(True),
            )
            .all()
        )

    def get_by_name_and_not_id(self, id_, name):
        return (
            self.query(self.model).filter(
                self.model.name == name,
                self.model.id != id_,
            ).one()
        )

    def get_avalible_games_view(self, convent_id):
        return (
            self.query(Game.name, GameEntity, User)
            .join(GameCopy)
            .join(GameEntity)
            .join(User)
            .filter(GameEntity.convent_id == convent_id)
            .order_by(User.name, Game.name)
        )

    def top_games_view(self, convent):
        return (
            self.query(
                func.count(GameBorrow.id).label('borrows'),
                Game.name)
            .join(GameEntity)
            .join(GameCopy)
            .join(Game)
            .group_by(Game.id)
            .order_by(desc('borrows'))
            .filter(GameEntity.convent == convent)
            .all()
        )

    def games_count_for_convent_view(self, convent):
        return (
            self.query(func.count(distinct(Game.id)))
            .join(GameCopy)
            .join(GameEntity)
            .filter(
                GameEntity.convent == convent,
                Game.is_active.is_(True),
            )
            .scalar())
