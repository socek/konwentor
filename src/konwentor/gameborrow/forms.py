from datetime import datetime

from formskit import Field
from formskit.field import AvalibleValue
from formskit.converters import ToInt
from formskit.formvalidators import FormValidator
from formskit.validators import NotEmpty, IsDigit, IsValueInAvalibleValues
from sqlalchemy.orm.exc import NoResultFound

from konwentor.application.translations import KonwentorForm

from .models import GameBorrow
from konwentor.game.models import Game
from konwentor.gamecopy.models import GameEntity, GameCopy
from konwentor.auth.models import User


class GameBorrowAddForm(KonwentorForm):

    def create_form(self):
        self.add_field(
            'game_entity_id',
            validators=[NotEmpty()])
        self.add_field(
            'name',
            label='Imię',
            validators=[NotEmpty()])
        self.add_field(
            'surname',
            label='Nazwisko',
            validators=[NotEmpty()])
        field = Field(
            'document_type',
            label='Dokument',
            validators=[NotEmpty()])
        field.data = self.get_avalible_documents
        self.add_field_object(field)
        self.add_field(
            'document_number',
            label='Numer dokumentu',
            validators=[NotEmpty()])

    def get_avalible_documents(self):
        return [
            {
                'label': '(Wybierz)',
                'value': '',
            },
            {
                'label': 'Dowód',
                'value': 'dowód',
            },
            {
                'label': 'Legitymacja',
                'value': 'legitymacja',
            },
            {
                'label': 'Prawo Jazdy',
                'value': 'prawo jazdy',
            },
            {
                'label': 'Paszport',
                'value': 'paszport',
            },
            {
                'label': 'Inne',
                'value': 'inne',
            }
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
        element.surname = data['surname']
        element.set_document(data['document_type'], data['document_number'])
        element.borrowed_timestamp = datetime.utcnow()

        element.is_borrowed = True

        self.db.add(element)
        self.db.commit()

    def get_entity(self, entity_id):
        return (
            self.db.query(GameEntity)
            .filter_by(id=entity_id)
            .one())


class GameBorrowReturnForm(KonwentorForm):

    def create_form(self):
        self.add_field(
            'game_borrow_id',
            validators=[NotEmpty(), IsDigit()],
            convert=ToInt())
        field = self.add_field(
            'game_entity_id',
            label='Wypożycza',
            validators=[IsValueInAvalibleValues()])
        field.set_avalible_values(self.get_game_names_for_select)
        self.add_field(
            'convent_id',
            validators=[NotEmpty(), IsDigit()],
            convert=ToInt())

        self.add_form_validator(IsGameBorrowExisting())

    def get_avalible_games(self):
        query = (
            self.query(Game.name, GameEntity, User)
            .join(GameCopy)
            .join(GameEntity)
            .join(User)
            .filter(GameEntity.convent_id == self.get_value('convent_id'))
            .order_by(User.name, Game.name)
        )
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
        return (
            self.form.query(GameBorrow)
            .filter_by(id=id_)
            .one())
