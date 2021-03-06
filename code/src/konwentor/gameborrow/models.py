from datetime import datetime

from haplugin.sql import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class GameBorrow(Base):
    __tablename__ = 'game_borrows'

    id = Column(
        Integer,
        primary_key=True)
    game_entity_id = Column(
        Integer,
        ForeignKey('game_entities.id'),
        nullable=False)
    borrowed_timestamp = Column(
        DateTime,
        default=datetime.now,
        nullable=False)
    return_timestamp = Column(
        DateTime)
    is_borrowed = Column(Boolean)

    name = Column(String)
    document = Column(String)

    gameentity = relationship("GameEntity", backref='borrows')

    def get_return_timestamp(self):
        try:
            return self.return_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        except AttributeError:
            return ''
