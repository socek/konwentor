from konwentor.application.driver import KonwentorDriver

from .models import Room


def get_one_of(names, kwargs):
    values = []
    for name in names:
        if kwargs.get(name, None):
            values.append(kwargs[name])

    if len(values) != 1:
        raise AttributeError('Need one of: %s' % (', '.join(names)))

    return values[0]


class RoomDriver(KonwentorDriver):
    name = 'Room'
    model = Room

    def create(self, name, **kwargs):
        get_one_of(('convent_id', 'convent'), kwargs)

        return super().create(name=name, **kwargs)
