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
            self.query(GameBorrow.name)
            .group_by(GameBorrow.name)
            .join(GameEntity)
            .filter(GameEntity.convent == convent)
        )

    def peoples_view(self, convent):
        return (
            self.query(
                GameBorrow.name.label('name'),
                func.count(GameBorrow.id).label('borrows'),)
            .join(GameEntity)
            .group_by(GameBorrow.name)
            .order_by(desc('borrows'))
            .filter(GameEntity.convent == convent)
            .all()
        )
