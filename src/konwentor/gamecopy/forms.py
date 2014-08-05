from formskit import Field

from konwentor.application.forms import PostForm
from konwentor.forms.validators import NotEmpty, IsDigit
from konwentor.auth.models import User

from .models import GameCopy, GameCopyOnConvent


class GameCopyAddForm(PostForm):

    def createForm(self):
        self.addField(
            Field('name', label='Nazwa gry', validators=[NotEmpty()]))

        field = Field(
            'user_id',
            label='Właściciel',
            validators=[NotEmpty(), IsDigit])
        field.data = self.get_users()
        self.addField(field)

    def get_users(self):
        users = [{
            'label': '(Wybierz)',
            'value': '',
        }]
        for user in self.db.query(User).all():
            users.append({
                'label': user.name,
                'value': user.id,
            })
        return users

    # def submit(self, data):
    #     element = Game(name=data['name'][0])
    #     self.db.add(element)
    #     self.db.commit()
