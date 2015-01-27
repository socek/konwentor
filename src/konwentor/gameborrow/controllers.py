from datetime import datetime
from collections import namedtuple

from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy.orm.exc import NoResultFound

from hatak.controller import Controller, JsonController
from haplugin.formskit.helpers import FormWidget

from .forms import GameBorrowAddForm, GameBorrowReturnForm
from .models import GameBorrow, make_hash_document
from konwentor.gamecopy.controllers import GameCopyControllerBase
from konwentor.gamecopy.models import GameEntity
from konwentor.application.translations import KonwentorMessage


class GameBorrowAddController(Controller):

    template = 'gameborrow:add.jinja2'
    permissions = [('gameborrow', 'add'), ]
    menu_highlighted = ''

    def make(self):
        self.data['game_entity'] = self.get_game_entity()
        form = self.add_form(GameBorrowAddForm)
        form.set_value('game_entity_id', self.data['game_entity'].id)

        if form.validate():
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

        self.process_form()
        self.prepere_template()

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

    def process_form(self):
        form = GameBorrowReturnForm(self.request)
        form.set_value('convent_id', self.session['convent_id'])

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
        self.redirect('gameborrow:list', True)

    def _on_form_fail(self, form):
        game_entity_id = form.fields['game_entity_id']

        if form.message:
            message = KonwentorMessage(form.message())
        else:
            message = KonwentorMessage(game_entity_id.get_value_error())

        self.add_flashmsg(message(), 'danger')

    def prepere_template(self):
        self.data['convent'] = self.get_convent()
        self.data['borrows'] = self.get_borrows(self.data['convent'])
        self.data['logs'] = self.generate_log(self.data['convent'])
        for borrow in self.data['borrows']:
            form = GameBorrowReturnForm(self.request)
            form.set_value('game_borrow_id', borrow.id)
            form.set_value('convent_id', self.session['convent_id'])
            borrow.form = FormWidget(self.request, form)


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


class ShowPersonHint(JsonController):
    permissions = [('gameborrow', 'add'), ]
    document_types = [
        'dowód',
        'legitymacja',
        'prawo jazdy',
        'paszport',
        'inne',
    ]

    def make(self):
        number = self.POST['number']
        obj = self.get_hint(number)
        self.data['name'] = obj.name
        self.data['surname'] = obj.surname
        self.data['document'] = obj.document

    def get_hint(self, number):
        for document in self.document_types:
            try:
                return self.get_values_by_document_and_number(document, number)
            except AttributeError:
                # obj is a None, so we need to search further
                pass

        obj = namedtuple('Result', ['name', 'surname', 'document'])('', '', '')
        return obj

    def get_values_by_document_and_number(self, document, number):
        hashed = make_hash_document(self.request, document, number)
        obj = self.get_game_borrow_by_stat_hash(hashed)
        obj.document = document
        return obj

    def get_game_borrow_by_stat_hash(self, hashed):
        return (
            self.db.query(
                GameBorrow.name,
                GameBorrow.surname,
            )
            .filter(GameBorrow.stats_hash == hashed)
            .order_by(GameBorrow.borrowed_timestamp.desc())
            .first()
        )
