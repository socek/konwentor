from formskit.validators import NotEmpty, IsDigit
from formskit.converters import ToInt

from konwentor.application.translations import KonwentorForm


class GameCopyAddForm(KonwentorForm):

    def create_form(self):
        field = self.add_field(
            'game_name',
            label='Gra',
            validators=[NotEmpty()])
        field.set_avalible_values(self.get_objects('Game', is_active=True))

        self.add_field(
            'confirmation',
            validators=[])

        field = self.add_field(
            'user_id',
            label='Właściciel',
            validators=[NotEmpty(), IsDigit()],
            convert=ToInt())
        field.set_avalible_values(self.get_objects('User'))

        field = self.add_field(
            'room_id',
            label='Pokój',
            validators=[NotEmpty(), IsDigit()],
            convert=ToInt())

        self.add_field(
            'count',
            label='Ilość',
            validators=[NotEmpty(), IsDigit()],
            convert=ToInt())

    def get_objects(self, driver_name, other=False, **kwargs):
        def generator():
            yield {
                'label': '(Wybierz)',
                'value': '',
            }
            driver = getattr(self.driver, driver_name)
            for obj in driver.get_objects(**kwargs).all():
                yield {
                    'label': obj.name,
                    'value': obj.id,
                }
            if other:
                yield {
                    'label': '',
                    'value': '-1',
                }
        return generator

    def on_success(self):
        data = self.get_data_dict(True)
        game = self.get_or_create_game(data['game_name'])
        user = self.driver.User.get_by_id(data['user_id'])
        room = self.driver.Room.get_by_id(data['room_id'])

        gamecopy = self.create_gamecopy(game, user)
        gameentity = self.create_gameentity(room, gamecopy)
        self.db.flush()
        gameentity.count += data['count']

        try:
            self.db.commit()
        finally:
            self.db.rollback()

    def get_or_create_game(self, name):
        return self.driver.Game.get_or_create(name=name, is_active=True)

    def create_gamecopy(self, game, user):
        gamecopy = self.driver.GameCopy.get_or_create(
            game=game,
            owner=user)
        return gamecopy

    def create_gameentity(self, room, gamecopy):
        return self.driver.GameEntity.get_or_create(
            convent=room.convent,
            gamecopy=gamecopy,
            room=room,
        )
