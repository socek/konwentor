from sqlalchemy import func

from konwentor.application.driver import KonwentorDriver

from .models import GameCopy, GameEntity


class GameCopyDriver(KonwentorDriver):
    name = 'GameCopy'
    model = GameCopy

    def count_for_convent(self, convent):
        return (
            self.query(func.sum(GameEntity.count))
            .filter(GameEntity.convent == convent)
            .scalar()
        )


class GameEntityDriver(KonwentorDriver):
    name = 'GameEntity'
    model = GameEntity

    def get_for_convent_and_id(self, convent, obj_id):
        return (
            self.query(GameEntity)
            .filter(
                GameEntity.convent_id == convent.id,
                GameEntity.id == obj_id,
            )
            .one()
        )
