from hatak.controller import Controller


class RoomController(Controller):

    def second_filter(self):
        super().before_filter()
        self.data['room_id'] = self.get_room_id()

    def get_room_id(self):
        return self.matchdict['room_id']

    # def get_room_object(self):
