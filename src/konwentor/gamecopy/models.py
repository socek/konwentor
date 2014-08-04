from hatak.db import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class GameCopy(Base):
    __tablename__ = 'game_copies'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    game = relationship("Game", backref='copies')
    owner = relationship("User", backref='games')


class GameCopyOnConvent(Base):
    __tablename__ = 'game_copies_2_convents'

    id = Column(Integer, primary_key=True)
    count = Column(Integer, nullable=False, default=1)
    gamecopy_id = Column(Integer, ForeignKey('game_copies.id'), nullable=False)
    convent_id = Column(Integer, ForeignKey('convents.id'), nullable=False)

    gamecopy = relationship("GameCopy", backref='on_convent')
    convent = relationship("Convent", backref="game_copies")
