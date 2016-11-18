from haplugin.jinja2 import Jinja2HelperSingle

from konwentor.menu.models import MenuObject


class RoomMenuObject(MenuObject):

    def get_room_id(self):
        return self.route_args[1].get('room_id', None)

    def is_highlited(self):
        room_id = self.get_room_id()
        url_room_id = self.request.matchdict.get('room_id', None)
        return self.highlighted == self.route and url_room_id == str(room_id)


class SideMenuWidget(Jinja2HelperSingle):

    template = 'konwentor.menu:templates/side.jinja2'

    def __init__(self, request, highlighted):
        super().__init__(request)
        self.highlighted = highlighted

    def add_menu(self, *args, **kwargs):
        menu = MenuObject(self, *args, **kwargs)
        self.data['menu'].append(menu)
        return menu

    def make(self):
        self.data['menu'] = []
        self.convent = self.driver.Convent.get_convent_from_session(
            self.request
        )

        for room in self.convent.rooms:
            submenu = self.add_menu(room.name, None, 'star')
            submenu.add_child_object(
                RoomMenuObject(
                    submenu.widget,
                    'Dodaj grę',
                    'gamecopy:add',
                    'magic',
                    room_id=room.id,
                    convent_id=room.convent_id,
                )
            )
            submenu.add_child_object(
                RoomMenuObject(
                    submenu.widget,
                    'Lista gier',
                    'gamecopy:list',
                    'magic',
                    room_id=room.id,
                    convent_id=room.convent_id,
                )
            )
            submenu.add_child_object(
                RoomMenuObject(
                    submenu.widget,
                    'Lista wypożyczeń',
                    'gameborrow:list',
                    'magic',
                    room_id=room.id,
                    convent_id=room.convent_id,
                )
            )
        submenu = self.add_menu('Misc', None, 'star')
        submenu.add_child(
            'Statystyki',
            'statistics:all',
            'magic',
            convent_id=self.request.matchdict['convent_id'],
        )
