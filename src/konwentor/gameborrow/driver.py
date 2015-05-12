from sqlalchemy import func, desc

from konwentor.application.driver import KonwentorDriver

from .models import GameBorrow
from konwentor.gamecopy.models import GameEntity


class GameBorrowDriver(KonwentorDriver):
    name = 'GameBorrow'
    model = GameBorrow

    def get_borrowed_for_room(self, room):
        return (
            self.query(GameBorrow)
            .join(GameEntity)
            .filter(GameEntity.room == room)
            .filter(GameBorrow.is_borrowed.is_(True))
            .all()
        )

    def get_returned_for_room(self, room):
        return (
            self.query(GameBorrow)
            .join(GameEntity)
            .filter(GameEntity.room == room)
            .filter(GameBorrow.is_borrowed.is_(False))
            .all()
        )

    def get_for_convent(self, convent):
        return (
            self.query(GameBorrow)
            .join(GameEntity)
            .filter(GameEntity.convent == convent)
            .all()
        )

    def get_people_for_convent(self, convent):
        return (
            self.query(GameBorrow.stats_hash)
            .group_by(GameBorrow.stats_hash)
            .join(GameEntity)
            .filter(GameEntity.convent == convent)
        )

    def get_by_hash_view(self, hashed):
        return (
            self.db.query(
                GameBorrow.name,
                GameBorrow.surname,
            )
            .filter(GameBorrow.stats_hash == hashed)
            .order_by(GameBorrow.borrowed_timestamp.desc())
            .first()
        )

    def peoples_view(self, convent):
        return (
            self.query(
                func.max(GameBorrow.name).label('name'),
                func.min(GameBorrow.surname).label('surname'),
                func.count(GameBorrow.id).label('borrows'),)
            .join(GameEntity)
            .group_by(GameBorrow.stats_hash)
            .order_by(desc('borrows'))
            .filter(GameEntity.convent == convent)
            .all()
        )
