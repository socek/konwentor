from hatak.db import Base
from sqlalchemy import Column, Integer, String


class Convent(Base):
    __tablename__ = 'convents'

    id = Column(Integer, primary_key=True)
    name = Column(String)
