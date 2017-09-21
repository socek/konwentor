from konwentor.application.driver import KonwentorDriver

from .models import Convent


class ConventDriver(KonwentorDriver):
    name = 'Convent'
    model = Convent

    def get_actives(self):
        return self.find_all().filter_by(is_active=True)

    def get_active(self, obj_id):
        return (
            self.query(self.model)
            .filter_by(id=obj_id, is_active=True)
            .one()
        )

    def get_convent_from_session(self, request):
        id_ = request.matchdict.get('convent_id', None)
        return self.get_by_id(id_)
