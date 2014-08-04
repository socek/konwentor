from hatak.db import Base
from sqlalchemy import Column, Integer, String


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
