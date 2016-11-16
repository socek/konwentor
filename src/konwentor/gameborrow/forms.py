from datetime import datetime

from formskit.converters import ToInt
from formskit.field import AvalibleValue
from formskit.formvalidators import FormValidator
from formskit.validators import IsDigit
from formskit.validators import IsValueInAvalibleValues
from formskit.validators import NotEmpty
from sqlalchemy.orm.exc import NoResultFound

from konwentor.application.translations import KonwentorForm

from .models import GameBorrow


class GameBorrowAddForm(KonwentorForm):

    def create_form(self):
        self.add_field(
            'game_entity_id',
            validators=[NotEmpty()])
        self.add_field(
            'name',
            label='Nazwa',
            validators=[NotEmpty()])
        field = self.add_field(
            'document',
            label='Dokument',
            validators=[NotEmpty()])

        field.set_avalible_values(self.get_avalible_documents)

    def get_avalible_documents(self):
        return [
            {
                'label': 'Inne',
                'value': 'inne', },
            {
                'label': 'Dowód',
                'value': 'dowód', },
            {
                'label': 'Legitymacja',
                'value': 'legitymacja', },
            {
                'label': 'Prawo Jazdy',
                'value': 'prawo jazdy', },
            {
                'label': 'Paszport',
                'value': 'paszport', },
        ]

    def overal_validation(self, data):
        entity = self.get_entity(data['game_entity_id'][0])
        if entity.is_avalible():
            return True
        else:
            self.message = 'Ta gra nie ma już wolnych kopii.'
            return False

    def on_success(self):
        data = self.get_data_dict(True)
        element = GameBorrow()
        element.assign_request(self.request)
        element.game_entity_id = data['game_entity_id']
        element.name = data['name']
        element.document = data['document']
        element.borrowed_timestamp = datetime.utcnow()

        element.is_borrowed = True

        self.db.add(element)
        self.db.commit()

    def get_entity(self, entity_id):
        return self.driver.GameEntity.get_by_id(entity_id)


class GameBorrowReturnForm(KonwentorForm):

    def create_form(self):
        self.add_field(
            'game_borrow_id',
            validators=[NotEmpty(), IsDigit()],
            convert=ToInt())
        field = self.add_field(
            'game_entity_id',
            label='Wypożycza',
            validators=[IsValueInAvalibleValues(allow_empty=True)],
            convert=ToInt())
        field.set_avalible_values(self.get_entity_ids)
        self.add_field(
            'room_id',
            validators=[NotEmpty(), IsDigit()],
            convert=ToInt())

        self.add_form_validator(IsGameBorrowExisting())

    def get_avalible_games(self):
        query = self.driver.Game.get_avalible_games_view(
            self.get_value('room_id'))
        for game in query:
            if game.GameEntity.is_avalible():
                yield game

    def get_entity_ids(self):
        yield AvalibleValue('', '(nie wypożycza)')
        for game in self.get_avalible_games():
            yield AvalibleValue(
                game.GameEntity.id,
                '{owner} - {name}'.format(
                    name=game.name,
                    owner=game.User.name
                ),
            )

    def on_success(self):
        self.return_game()
        self.borrow_next()
        self.db.flush()
        self.db.commit()

    def return_game(self):
        # self.borrow is made by IsGameBorrowExisting validator
        self.borrow.is_borrowed = False
        self.borrow.return_timestamp = datetime.utcnow()

    def borrow_next(self):
        if self.get_value('game_entity_id'):
            self.new_borrow = GameBorrow()
            self.new_borrow.assign_request(self.request)
            self.new_borrow.game_entity_id = self.get_value('game_entity_id')
            self.new_borrow.name = self.borrow.name
            self.new_borrow.surname = self.borrow.surname
            self.new_borrow.stats_hash = self.borrow.stats_hash
            self.new_borrow.is_borrowed = True
            self.new_borrow.borrowed_timestamp = datetime.utcnow()

            self.db.add(self.new_borrow)


class IsGameBorrowExisting(FormValidator):

    message = 'Game Had been returned earlier.'

    def validate(self):
        try:
            self.form.borrow = self.get_borrow(
                self.form.get_value('game_borrow_id'))
            return True
        except NoResultFound:
            return False

    def get_borrow(self, id_):
        return self.form.driver.GameBorrow.get_by_id(id_)
