from formskit import Field

from konwentor.forms.models import PostForm
from konwentor.forms.validators import NotEmpty

from konwentor.gamecopy.models import GameEntity
from .models import GameBorrow


class GameBorrowAddForm(PostForm):

    def createForm(self):
        self.addField(Field(
            'game_entity_id',
            validators=[NotEmpty()]))
        self.addField(Field(
            'name',
            label='Imię',
            validators=[NotEmpty()]))
        self.addField(Field(
            'surname',
            label='Nazwisko',
            validators=[NotEmpty()]))
        field = Field(
            'document_type',
            label='Dokument',
            validators=[NotEmpty()])
        field.data = self.get_avalible_documents()
        self.addField(field)
        self.addField(Field(
            'document_number',
            label='Numer dokumentu',
            validators=[NotEmpty()]))

    def get_avalible_documents(self):
        objects = [
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
        return objects

    def overalValidation(self, data):
        entity = self.get_entity(data['game_entity_id'][0])
        if entity.is_avalible():
            return True
        else:
            self.message = 'Ta gra nie ma już wolnych kopii.'
            return False

    def submit(self, data):
        element = GameBorrow()
        element.game_entity_id = data['game_entity_id'][0]
        element.name = data['name'][0]
        element.surname = data['surname'][0]
        element.document_type = data['document_type'][0]
        element.document_number = data['document_number'][0]

        element.is_borrowed = True

        self.db.add(element)
        self.db.commit()

    def get_entity(self, entity_id):
        return (
            self.db.query(GameEntity)
            .filter_by(id=entity_id)
            .one())
