from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from haplugin.sql import Base


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    convent_id = Column(Integer, ForeignKey('convents.id'), nullable=False)

    convent = relationship("Convent", backref='rooms')

    def __repr__(self):
        data = super().__repr__()
        return '%s: %s' % (data, self.name)
