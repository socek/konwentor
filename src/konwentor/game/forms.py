from sqlalchemy.orm.exc import NoResultFound
from formskit import Field

from konwentor.convent.forms import IdExists
from konwentor.forms.models import PostForm
from konwentor.forms.validators import NotEmpty, IsDigit

from .models import Game


class GameAddForm(PostForm):

    def createForm(self):
        self.addField(Field('name', label='Nazwa', validators=[NotEmpty()]))

    def overalValidation(self, data):
        if self.validate_uniqe_name(data['name'][0]):
            return True
        else:
            self.message = 'Gra o takiej nazwie już istnieje.'
            return False

    def validate_uniqe_name(self, name):
        try:
            self.query(Game).filter_by(name=name).one()
            return False
        except NoResultFound:
            return True

    def set_values(self, element, data):
        element.name = data['name'][0]

    def submit(self, data):
        element = Game()
        self.set_values(element, data)
        self.db.add(element)
        self.db.commit()


class GameEditForm(GameAddForm):

    def createForm(self):
        super().createForm()
        self.addField(Field('id', validators=[NotEmpty(), IsDigit()]))

        self.addFormValidator(IdExists(Game))

    def submit(self, data):
        self.set_values(self.model, data)
        self.db.commit()


class GameDeleteForm(PostForm):

    def createForm(self):
        self.addField(Field('obj_id', validators=[NotEmpty()]))

    def submit(self, data):
        _id = data['obj_id'][0]
        element = self.db.query(Game).filter_by(id=_id).one()
        element.is_active = False
        self.db.commit()
