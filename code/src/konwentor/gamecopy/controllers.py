from hatak.controller import Controller
from hatak.controller import EndController
from pyramid.httpexceptions import HTTPOk
from sqlalchemy.orm.exc import NoResultFound

from konwentor.convent.helpers import ConventWidget
from konwentor.gameborrow.sidemenu import SideMenuWidget

from .forms import GameCopyAddForm
from .helpers import GameEntityWidget
from konwentor.room.controller import RoomController


class ConventController(Controller):
    menu_highlighted = None

    def second_filter(self):
        super().second_filter()
        self.verify_convent()
        self.convent = self.get_convent()

    def verify_convent(self):
        if 'convent_id' not in self.session:
            self.add_flashmsg('Proszę wybrać konwent.', 'danger')
            self.redirect('convent:list')
            return False
        return True

    def get_convent(self):
        try:
            return self.driver.Convent.get_active(self.session['convent_id'])
        except NoResultFound:
            self.add_flashmsg('Proszę wybrać konwent.', 'danger')
            self.redirect('convent:list')
            raise EndController()

    def make_helpers(self):
        super().make_helpers()
        self.add_helper('convent', ConventWidget, self.get_convent())
        self.add_helper('sidemenu', SideMenuWidget, self.menu_highlighted)


class GameCopyControllerBase(RoomController, ConventController):
    pass


class GameCopyAddController(GameCopyControllerBase):

    template = 'gamecopy:add.jinja2'
    permissions = [('gamecopy', 'add'), ]
    menu_highlighted = 'gamecopy:add'

    def make(self):
        if not self.verify_convent():
            return

        self.db.flush()

        form = self.prepere_form()

        if form.validate():
            self.add_flashmsg('Dodano grę.', 'info')
            self.session['last_user_id'] = form.get_value('user_id')
            self.redirect(
                'gamecopy:add',
                room_id=self.get_room_id(),
                convent_id=self.get_convent_id())

    def prepere_form(self):
        form = self.add_form(GameCopyAddForm)
        initial_data = {
            'count': 1,
            'user_id': self.user.id,
            'room_id': self.get_room_id(),
        }

        if 'last_user_id' in self.session:
            initial_data['user_id'] = self.session['last_user_id']

        form.parse_dict(initial_data)

        return form


class GameCopyListController(GameCopyControllerBase):

    template = 'gamecopy:list.haml'
    permissions = [('base', 'view'), ]
    menu_highlighted = 'gamecopy:list'

    def make(self):
        if not self.verify_convent():
            return

        self.data['convent'] = self.get_convent()
        self.data['games'] = [
            GameEntityWidget(self.request, obj) for obj
            in self.get_games(self.get_room())
        ]

    def get_games(self, room):
        return self.driver.Game.get_game_list_view(room)


class GameCopyListBoxController(GameCopyControllerBase):

    template = 'gamecopy:listbox.haml'
    permissions = [('base', 'view'), ]
    menu_highlighted = 'gamecopy:listbox'

    def make(self):
        if not self.verify_convent():
            return

        room = self.get_room()
        self.data['convent'] = self.get_convent()
        self.data['games_in_box'] = self.get_games_in_box(room)
        self.data['games_outside_box'] = self.get_games_outside_box(room)

    def get_games_in_box(self, room):
        for game in self.driver.Game.get_game_listbox_view(room, True):
            yield GameEntityWidget(self.request, game)

    def get_games_outside_box(self, room):
        for game in self.driver.Game.get_game_listbox_view(room, False):
            yield GameEntityWidget(self.request, game)


class GameCopyToBoxController(GameCopyControllerBase):

    permissions = [('gamecopy', 'add'), ]

    def make(self):
        if not self.verify_convent():
            return

        self.move_to_box()
        self.response = HTTPOk()

    def move_to_box(self):
        convent = self.get_convent()
        entity = self.get_game_entity(convent)
        entity.move_to_box()
        self.db.commit()

    def get_game_entity(self, convent):
        return self.driver.GameEntity.get_for_convent_and_id(
            convent, self.matchdict['obj_id']
        )
