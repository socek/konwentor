from formskit import Field

from konwentor.application.forms import PostForm
from konwentor.forms.validators import NotEmpty

from .models import Game


class GameAddForm(PostForm):

    def createForm(self):
        self.addField(Field('name', label='Nazwa', validators=[NotEmpty()]))

    def submit(self, data):
        element = Game(name=data['name'][0])
        self.db.add(element)
        self.db.commit()


class GameDeleteForm(PostForm):

    def createForm(self):
        self.addField(Field('obj_id', validators=[NotEmpty()]))

    def submit(self, data):
        element = self.db.query(Game).filter_by(id=data['obj_id'][0]).one()
        element.remove(self.db)
        self.db.commit()
