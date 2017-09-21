from hatak.controller import Controller, EndController


class RoomController(Controller):

    def second_filter(self):
        super().second_filter()
        self.data['room_id'] = self.get_room_id()
        if self.data['room_id'] == 0:
            room_id = self.convent.rooms[0].id
            self.redirect(
                'gamecopy:list',
                room_id=room_id,
                convent_id=self.get_convent_id())
            raise EndController()

    def get_room_id(self):
        return int(self.matchdict['room_id'])

    def get_room(self):
        return self.driver.Room.get_by_id(self.get_room_id())

    def get_convent_id(self):
        return int(self.matchdict['convent_id'])
