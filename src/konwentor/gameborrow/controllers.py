from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from pyramid.httpexceptions import HTTPNotFound

from hatak.controller import Controller

from .forms import GameBorrowAddForm
from .models import GameBorrow
from konwentor.gamecopy.controllers import GameCopyControllerBase
from konwentor.gamecopy.models import GameEntity


class GameBorrowAddController(Controller):

    template = 'gameborrow:add.jinja2'
    permissions = [('gameborrow', 'add'), ]
    menu_highlighted = ''

    def make(self):
        self.data['game_entity'] = self.get_game_entity()
        form = self.add_form(GameBorrowAddForm)

        if form({'game_entity_id': [self.data['game_entity'].id]}):
            self.add_flashmsg('Gra została wypożyczona.', 'success')
            self.redirect('gamecopy:list')

    def get_game_entity(self):
        try:
            return (
                self.query(GameEntity)
                .filter_by(id=self.matchdict['obj_id'])
                .one())
        except NoResultFound:
            raise HTTPNotFound()


class GameBorrowListController(GameCopyControllerBase):
    template = 'gameborrow:list.jinja2'
    permissions = [('base', 'view'), ]
    menu_highlighted = 'gameborrow:list'

    def make(self):
        if not self.verify_convent():
            return

        self.data['convent'] = self.get_convent()
        self.data['borrows'] = self.get_borrows(self.data['convent'])
        self.data['logs'] = self.generate_log(self.data['convent'])

    def get_borrows(self, convent):
        return (
            self.db.query(GameBorrow)
            .join(GameEntity)
            .filter(GameEntity.convent == convent)
            .filter(GameBorrow.is_borrowed.is_(True))
            .all())

    def generate_log(self, convent):
        return (
            self.db.query(GameBorrow)
            .join(GameEntity)
            .filter(GameEntity.convent == convent)
            .filter(GameBorrow.is_borrowed.is_(False))
            .all())


class GameBorrowReturnController(Controller):

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
            return (
                self.query(GameBorrow)
                .filter_by(id=self.matchdict['obj_id'])
                .one())
        except NoResultFound:
            raise HTTPNotFound()