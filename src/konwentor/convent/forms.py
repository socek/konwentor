from formskit import Field
from formskit.formvalidators import FormValidator
from sqlalchemy.orm.exc import NoResultFound

from haplugin.formskit import PostForm
from konwentor.forms.validators import NotEmpty, IsDigit

from .models import Convent


class ConventAddForm(PostForm):

    def createForm(self):
        self.addField(Field('name', label='Nazwa', validators=[NotEmpty()]))

    def submit(self, data):
        Convent.create(self.db, name=data['name'][0])


class ConventEditForm(ConventAddForm):

    def createForm(self):
        super().createForm()
        self.addField(Field('id', validators=[NotEmpty(), IsDigit()]))

        self.addFormValidator(IdExists(Convent))

    def submit(self, data):
        self.model.name = self.get_value('name')
        self.db.commit()


class ConventDeleteForm(PostForm):

    def createForm(self):
        self.addField(Field('obj_id', validators=[NotEmpty()]))

    def submit(self, data):
        convent = Convent.get_by_id(self.db, int(data['obj_id'][0]))
        convent.is_active = False
        self.db.commit()


class IdExists(FormValidator):
    message = 'Obiekt nie istnieje.'

    def __init__(self, model_class):
        self.model_class = model_class

    def validate(self):
        id_ = self.form.get_value('id')
        db = self.form.db
        try:
            self.form.model = self.model_class.get_by_id(db, id_)
            return True
        except NoResultFound:
            return False
