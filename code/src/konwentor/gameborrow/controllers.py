from datetime import datetime

from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy.orm.exc import NoResultFound

from haplugin.formskit.helpers import FormWidget

from .forms import GameBorrowAddForm, GameBorrowReturnForm
from konwentor.gamecopy.controllers import GameCopyControllerBase
from konwentor.gameborrow.sidemenu import SideMenuWidget
from konwentor.room.controller import RoomController


class GameBorrowAddController(RoomController):

    template = 'gameborrow:add.jinja2'
    permissions = [('gameborrow', 'add'), ]
    menu_highlighted = ''

    def make(self):
        self.data['game_entity'] = self.get_game_entity()
        form = self.add_form(GameBorrowAddForm)
        form.set_value('game_entity_id', self.data['game_entity'].id)

        if form.validate():
            self.add_flashmsg('Gra została wypożyczona.', 'success')
            self.redirect(
                'gamecopy:list',
                room_id=self.get_room_id(),
                convent_id=self.get_convent_id())

    def get_game_entity(self):
        try:
            return self.driver.GameEntity.get_by_id(self.matchdict['obj_id'])
        except NoResultFound:
            raise HTTPNotFound()

    def make_helpers(self):
        super().make_helpers()
        self.add_helper('sidemenu', SideMenuWidget, None)


class GameBorrowListController(GameCopyControllerBase):
    template = 'gameborrow:list.jinja2'
    permissions = [('base', 'view'), ]
    menu_highlighted = 'gameborrow:list'

    def make(self):
        if not self.verify_convent():
            return

        self.process_form()
        self.prepere_template()

    def get_borrows(self, convent):
        return self.driver.GameBorrow.get_borrowed_for_room(self.get_room())

    def generate_log(self, convent):
        return self.driver.GameBorrow.get_returned_for_room(self.get_room())

    def process_form(self):
        form = GameBorrowReturnForm(self.request)
        form.set_value('room_id', self.get_room_id())

        if form.validate():
            self._on_form_success(form)

        if form.success is False:
            self._on_form_fail(form)

    def _on_form_success(self, form):
        game_entity_id = form.fields['game_entity_id']

        if game_entity_id.get_value(default=False):
            message = (
                'Gra "{game}" została zwrócona, a "{second_game}" została'
                ' pożyczona.'
                .format(
                    game=form.borrow.gameentity.gamecopy.game.name,
                    second_game=form.new_borrow.gameentity.gamecopy.game.name,
                )
            )
        else:
            message = 'Gra "{game}" została zwrócona.'.format(
                game=form.borrow.gameentity.gamecopy.game.name,
            )

        self.add_flashmsg(message, 'info')
        self.redirect(
            'gameborrow:list',
            room_id=form.get_value('room_id'),
            convent_id=self.matchdict['convent_id'])

    def _on_form_fail(self, form):
        game_entity_id = form.fields['game_entity_id']

        if form.messages:
            message = form.messages[0]()
        else:
            message = game_entity_id.get_value_errors()[0]

        self.add_flashmsg(message, 'danger')

    def prepere_template(self):
        self.data['convent'] = self.get_convent()
        self.data['borrows'] = self.get_borrows(self.data['convent'])
        self.data['logs'] = self.generate_log(self.data['convent'])
        for borrow in self.data['borrows']:
            form = GameBorrowReturnForm(self.request)
            form.set_value('game_borrow_id', borrow.id)
            form.set_value('room_id', self.get_room_id())
            borrow.form = FormWidget(self.request, form)


class GameBorrowReturnController(RoomController):

    permissions = [('gameborrow', 'add'), ]

    def make(self):
        borrow = self.get_borrow()

        if borrow.is_borrowed:
            self.return_game(borrow)
            self.add_flashmsg('Gra została oddana.', 'success')
        else:
            self.add_flashmsg('Gra została oddana wcześniej.', 'warning')

        self.redirect('gameborrow:list')

    def return_game(self, borrow):
        borrow.is_borrowed = False
        borrow.return_timestamp = datetime.utcnow()
        self.db.commit()

    def get_borrow(self):
        try:
            return self.driver.GameBorrow.get_by_id(self.matchdict['obj_id'])
        except NoResultFound:
            raise HTTPNotFound()
