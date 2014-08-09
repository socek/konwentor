from hatak.db import Base
from sqlalchemy import Column, Integer, String


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def remove(self, db):
        for copy in self.copies:
            for on_convent in copy.on_convent:
                db.delete(on_convent)
            db.delete(copy)
        db.delete(self)
