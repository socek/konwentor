from sqlalchemy.orm.exc import NoResultFound
from formskit import Field

from konwentor.forms.models import PostForm
from konwentor.forms.validators import NotEmpty

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

    def submit(self, data):
        element = Game(name=data['name'][0])
        self.db.add(element)
        self.db.commit()


class GameDeleteForm(PostForm):

    def createForm(self):
        self.addField(Field('obj_id', validators=[NotEmpty()]))

    def submit(self, data):
        try:
            element = self.db.query(Game).filter_by(id=data['obj_id'][0]).one()
            element.remove(self.db)
            self.db.commit()
        finally:
            self.db.rollback()
