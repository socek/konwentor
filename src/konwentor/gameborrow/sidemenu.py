from haplugin.jinja2 import Jinja2HelperSingle

from konwentor.menu.models import MenuObject


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
            submenu.add_child(
                'Dodaj grę',
                'gamecopy:add',
                'magic',
                room_id=room.id
            )
            submenu.add_child(
                'Lista gier',
                'gamecopy:list',
                'magic',
                room_id=room.id
            )
            submenu.add_child(
                'Lista wypożyczeń',
                'gameborrow:list',
                'magic',
                room_id=room.id
            )
            submenu.add_child(
                'Statystyki',
                'statistics:all',
                'magic'
            )
