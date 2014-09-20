from hatak.db import Base
from sqlalchemy import Column, Integer, String, Boolean


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    players_description = Column(String)
    time_description = Column(String)
    type_description = Column(String)
    difficulty = Column(String)
