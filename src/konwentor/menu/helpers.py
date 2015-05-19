from sqlalchemy.orm.exc import NoResultFound

from haplugin.jinja2 import Jinja2HelperSingle

from .models import MenuObject


class OnConventMenuObject(MenuObject):

    def __init__(self, widget):
        super().__init__(widget, 'Na konwencie', None, 'arrow-circle-down')
        try:
            convent = self.request.driver.Convent.get_convent_from_session(
                self.request
            )
            for room in convent.rooms:
                self.add_child(
                    room.name,
                    'gamecopy:add',
                    'magic',
                    room_id=room.id
                )
        except NoResultFound:
            # do nothing if there is no convent_id set
            pass

    def is_avalible(self):
        return 'convent_id' in self.session


class TopMenuWidget(Jinja2HelperSingle):

    template = 'konwentor.menu:templates/main.jinja2'

    def __init__(self, request, highlighted):
        super().__init__(request)
        self.highlighted = highlighted

    def add_menu(self, *args, **kwargs):
        return self.add_menu_object(MenuObject(self, *args, **kwargs))

    def add_menu_object(self, menu):
        self.data['menu'].append(menu)
        return menu

    def make(self):
        self.data['menu'] = []
        self.add_menu('Konwenty', 'convent:list', 'calendar')
        self.add_menu('Gry', 'game:list', 'gamepad')

        self.add_menu_object(OnConventMenuObject(self))
