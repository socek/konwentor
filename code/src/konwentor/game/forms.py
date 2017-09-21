from sqlalchemy.orm.exc import NoResultFound
from formskit.validators import NotEmpty, IsDigit

from haplugin.formskit import PostForm
from konwentor.convent.forms import IdExists


from .models import Game


class GameAddForm(PostForm):

    def create_form(self):
        self.add_field('name', label='Nazwa', validators=[NotEmpty()])
        self.add_field('players_description', label='Gracze')
        self.add_field('time_description', label='Czas')
        self.add_field('type_description', label='Typ')
        self.add_field('difficulty', label='Trudność')

    def overal_validation(self, data):
        if self.validate_uniqe_name(data['name'][0]):
            return True
        else:
            self.message = 'Gra o takiej nazwie już istnieje.'
            return False

    def validate_uniqe_name(self, name):
        try:
            self.driver.Game.get_by_name(name)
            return False
        except NoResultFound:
            return True

    def on_success(self):
        element = Game()
        data = self.get_data_dict(True)
        self.set_values(element, data)
        self.db.add(element)
        self.db.commit()

    def set_values(self, element, data):
        element.name = data['name']
        descriptions = [
            'players_description',
            'time_description',
            'type_description',
            'difficulty']
        for name in descriptions:
            value = data[name].strip()
            setattr(element, name, value)


class GameEditForm(GameAddForm):

    def create_form(self):
        super().create_form()
        self.add_field('id', validators=[NotEmpty(), IsDigit()])

        self.add_form_validator(IdExists('Game'))

    def on_success(self):
        data = self.get_data_dict(True)
        self.set_values(self.model, data)
        self.db.commit()

    def validate_uniqe_name(self, name):
        try:
            self.driver.Game.get_by_name_and_not_id(self.model.id, name)
            return False
        except NoResultFound:
            return True


class GameDeleteForm(PostForm):

    def create_form(self):
        self.add_field('obj_id', validators=[NotEmpty()])

    def on_success(self):
        data = self.get_data_dict(True)
        id_ = data['obj_id']
        element = self.driver.Game.get_by_id(id_)
        element.is_active = False
        self.db.commit()
