from formskit import Field
from formskit.validators import NotEmpty

from haplugin.formskit import PostForm

from konwentor.gamecopy.models import GameEntity
from .models import GameBorrow


class GameBorrowAddForm(PostForm):

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
        field.data = self.get_avalible_documents()
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

    def submit(self):
        data = self.get_data_dict(True)
        element = GameBorrow()
        element.game_entity_id = data['game_entity_id']
        element.name = data['name']
        element.surname = data['surname']
        element.document_type = data['document_type']
        element.document_number = data['document_number']

        element.is_borrowed = True

        self.db.add(element)
        self.db.commit()

    def get_entity(self, entity_id):
        return (
            self.db.query(GameEntity)
            .filter_by(id=entity_id)
            .one())
