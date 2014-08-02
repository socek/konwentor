from formskit import Field
from formskit.validators import NotEmpty

from konwentor.application.forms import PostForm

from .models import Convent


class NotEmptyPl(NotEmpty):
    message = 'Te pole nie może być puste!'


class ConventAddForm(PostForm):

    def createForm(self):
        self.addField(Field('name', label='Nazwa', validators=[NotEmptyPl()]))

    def submit(self, data):
        convent = Convent(name=data['name'][0])
        self.db.add(convent)
        self.db.commit()
