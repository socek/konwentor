from formskit import Field

from konwentor.forms.models import PostForm
from konwentor.forms.validators import NotEmpty

from .models import Convent


class ConventAddForm(PostForm):

    def createForm(self):
        self.addField(Field('name', label='Nazwa', validators=[NotEmpty()]))

    def submit(self, data):
        Convent.create(self.db, name=data['name'][0])


class ConventDeleteForm(PostForm):

    def createForm(self):
        self.addField(Field('obj_id', validators=[NotEmpty()]))

    def submit(self, data):
        Convent.delete_by_id(self.db, int(data['obj_id'][0]))
