from konwentor.application.driver import KonwentorDriver

from .models import Room


class RoomDriver(KonwentorDriver):
    name = 'Room'
    model = Room

    def create(self, name, convent_id, **kwargs):
        return super().create(name=name, convent_id=convent_id, **kwargs)
