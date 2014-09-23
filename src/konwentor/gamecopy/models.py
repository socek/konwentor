from hatak.plugins.sql import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class GameCopy(Base):
    __tablename__ = 'game_copies'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    game = relationship("Game", backref='copies')
    owner = relationship("User", backref='games')


class GameEntity(Base):
    __tablename__ = 'game_entities'

    id = Column(Integer, primary_key=True)
    count = Column(Integer, nullable=False, default=0)
    is_in_box = Column(Boolean, nullable=False, default=False)

    gamecopy_id = Column(Integer, ForeignKey('game_copies.id'), nullable=False)
    convent_id = Column(Integer, ForeignKey('convents.id'), nullable=False)

    gamecopy = relationship("GameCopy", backref='entities')
    convent = relationship("Convent", backref='entities')

    def active_borrows(self):
        for borrow in self.borrows:
            if borrow.is_borrowed:
                yield borrow

    def active_borrows_len(self):
        return len(list(self.active_borrows()))

    def is_avalible(self):
        return self.count > self.active_borrows_len()

    def move_to_box(self):
        self.is_in_box = True
