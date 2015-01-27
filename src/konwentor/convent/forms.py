from formskit.formvalidators import FormValidator
from formskit.validators import NotEmpty, IsDigit
from sqlalchemy.orm.exc import NoResultFound

from haplugin.formskit import PostForm

from .models import Convent


class ConventAddForm(PostForm):

    def create_form(self):
        self.add_field('name', label='Nazwa', validators=[NotEmpty()])

    def on_success(self):
        data = self.get_data_dict(True)
        Convent.create(self.db, name=data['name'])


class ConventEditForm(ConventAddForm):

    def create_form(self):
        super().create_form()
        self.add_field('id', validators=[NotEmpty(), IsDigit()])

        self.add_form_validator(IdExists(Convent))

    def on_success(self):
        self.model.name = self.get_value('name')
        self.db.commit()


class ConventDeleteForm(PostForm):

    def create_form(self):
        self.add_field('obj_id', validators=[NotEmpty()])

    def on_success(self):
        data = self.get_data_dict(True)
        convent = Convent.get_by_id(self.db, int(data['obj_id']))
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
