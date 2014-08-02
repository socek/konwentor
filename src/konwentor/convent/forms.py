from formskit import Field

from konwentor.application.forms import PostForm
from konwentor.forms.validators import NotEmpty

from .models import Convent


class ConventAddForm(PostForm):

    def createForm(self):
        self.addField(Field('name', label='Nazwa', validators=[NotEmpty()]))

    def submit(self, data):
        convent = Convent(name=data['name'][0])
        self.db.add(convent)
        self.db.commit()
