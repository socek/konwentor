from hatak.plugins.sql import Base
from sqlalchemy import Column, Integer, String, Boolean


class Convent(Base):
    __tablename__ = 'convents'

    STATES = (
        'not started',
        'running',
        'ended',
    )

    id = Column(Integer, primary_key=True)
    name = Column(String)
    _state = Column(
        'state', String(11), default=STATES[0], nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    def _get_state(self):
        return self._state

    def _set_state(self, value):
        if value not in self.STATES:
            raise RuntimeError('"%s" is invalid for state' % (value,))
        self._state = value

    state = property(_get_state, _set_state)

    def is_user_able_to_start(self, user):
        return (
            self.state == 'not started'
            and user.has_access_to_route('convent:start')
        )

    def is_user_able_to_end(self, user):
        return (
            self.state == 'running'
            and user.has_access_to_route('convent:end')
        )
