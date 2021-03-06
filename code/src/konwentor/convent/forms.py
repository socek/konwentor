from formskit.formvalidators import FormValidator
from formskit.validators import NotEmpty, IsDigit
from sqlalchemy.orm.exc import NoResultFound

from haplugin.formskit import PostForm

from .models import Convent


class ConventAddForm(PostForm):

    def create_form(self):
        self.add_field('name', label='Nazwa', validators=[NotEmpty()])
        self.add_field('room', label='Pokoje')

    def on_success(self):
        data = self.get_data_dict(False)
        convent = self.driver.Convent.create(name=data['name'][0])
        rooms = data.get('room', [])
        for room in rooms:
            if room.strip():
                self.driver.Room.create(name=room, convent=convent)

        self.db.commit()


class ConventEditForm(ConventAddForm):

    def create_form(self):
        super().create_form()
        self.add_field('id', validators=[NotEmpty(), IsDigit()])

        self.add_form_validator(IdExists('Convent'))

    def on_success(self):
        self.model.name = self.get_value('name')
        for index, name in enumerate(self.get_values('room')):
            if name.strip():
                try:
                    room = self.model.rooms[index]
                    room.name = name
                except IndexError:
                    self.driver.Room.create(name=name, convent=self.model)
        self.db.commit()


class ConventDeleteForm(PostForm):

    def create_form(self):
        self.add_field('obj_id', validators=[NotEmpty()])

    def on_success(self):
        data = self.get_data_dict(True)
        convent = self.driver.Convent.get_by_id(int(data['obj_id']))
        convent.is_active = False
        self.db.commit()


class IdExists(FormValidator):
    message = 'Obiekt nie istnieje.'

    def __init__(self, model_class):
        self.model_class = model_class

    def validate(self):
        id_ = self.form.get_value('id')
        driver = getattr(self.form.driver, self.model_class)
        try:
            self.form.model = driver.get_by_id(id_)
            return True
        except NoResultFound:
            return False
