from haplugin.toster import FormTestCase, SqlFormTestCase
from haplugin.toster.fixtures import fixtures
from sqlalchemy.orm.exc import NoResultFound

from ..forms import GameAddForm, GameDeleteForm, GameEditForm
from ..models import Game


class GameAddFormTest(FormTestCase):
    prefix_from = GameAddForm

    def test_overalValidation_success(self):
        """GameAddForm should check if there is game of the same name."""
        self.add_mock_object(self.form, 'validate_uniqe_name')
        self.mocks['validate_uniqe_name'].return_value = True

        result = self.form.overalValidation({'name': ['myname']})

        self.mocks['validate_uniqe_name'].assert_called_once_with('myname')
        self.assertEqual(True, result)

    def test_overalValidation_fail(self):
        self.add_mock_object(self.form, 'validate_uniqe_name')
        self.mocks['validate_uniqe_name'].return_value = False

        result = self.form.overalValidation({'name': ['myname']})

        self.mocks['validate_uniqe_name'].assert_called_once_with('myname')
        self.assertEqual(False, result)
        self.assertEqual(
            'Gra o takiej nazwie już istnieje.', self.form.message)


class SqlGameAddFormTests(SqlFormTestCase):
    prefix_from = GameAddForm

    def test_validate_uniqe_name_found(self):
        """validate_uniqe_name should return False if name found"""
        self.assertEqual(False, self.form.validate_uniqe_name('first'))

    def test_validate_uniqe_name_not_found(self):
        """validate_uniqe_name should return True if name not found"""
        self.assertEqual(True, self.form.validate_uniqe_name('firstasdasd'))

    def test_submit(self):
        """GameAddForm should create new game."""
        data = {
            'name': ['my dynamic name', ],
            'players_description': ['players description'],
            'time_description': ['time description'],
            'type_description': ['type description'],
            'difficulty': ['difficulty'],
        }
        self.form.submit(data)

        self.db.flush()
        game = self.query(Game).filter_by(name='my dynamic name').one()
        self.assertEqual('my dynamic name', game.name)
        self.assertEqual('players description', game.players_description)
        self.assertEqual('time description', game.time_description)
        self.assertEqual('type description', game.type_description)
        self.assertEqual('difficulty', game.difficulty)

        self.db.delete(game)
        self.db.commit()


class GameFactoryMixin(object):

    def create_game(self, name='my creazy name'):
        self.game = Game(name='my creazy name')
        self.db.add(self.game)
        self.db.commit()
        return self.game.id

    def delete_game(self):
        Game.delete_by_id(self.db, self.game.id)


class SqlGameDeleteFormTests(SqlFormTestCase, GameFactoryMixin):
    prefix_from = GameDeleteForm

    def test_submit(self):
        """GameDeleteForm should delete game"""
        self.create_game()

        try:
            self.form.submit({'obj_id': [self.game.id]})

            self.db.flush()
            self.assertRaises(
                NoResultFound,
                self.query(Game)
                    .filter_by(id=self.game.id, is_active=True).one)
        finally:
            self.delete_game()


class SqlGameEditFormTests(SqlFormTestCase, GameFactoryMixin):
    prefix_from = GameEditForm

    def test_submit(self):
        self.create_game()
        try:
            self._create_fake_post({
                'name': ['my mega name', ],
                'id': [str(self.game.id), ],
                'players_description': ['players description'],
                'time_description': ['time description'],
                'type_description': ['type description'],
                'difficulty': ['difficulty'],
            })
            self.assertEqual(True, self.form({'id': [str(self.game.id)]}))

            self.db.flush()
            game = self.query(Game).filter_by(id=self.game.id).one()
            self.assertEqual('my mega name', game.name)
            self.assertEqual('players description', game.players_description)
            self.assertEqual('time description', game.time_description)
            self.assertEqual('type description', game.type_description)
            self.assertEqual('difficulty', game.difficulty)
        finally:
            self.delete_game()

    def test_validate_uniqe_name_when_name_found(self):
        """validate_uniqe_name should return False if name is in database"""
        name = 'second'
        self.form.model = fixtures['Game']['first']
        self.assertEqual(False, self.form.validate_uniqe_name(name))

    def test_validate_uniqe_name_when_name_not_found(self):
        """validate_uniqe_name should return True if name is not in database"""
        name = 'New name'
        self.form.model = fixtures['Game']['first']
        self.assertEqual(True, self.form.validate_uniqe_name(name))

    def test_validate_uniqe_name_when_name_not_changed(self):
        """validate_uniqe_name should return True if name is in database but
        has the same id as our model"""
        name = 'first'
        self.form.model = fixtures['Game']['first']
        self.assertEqual(True, self.form.validate_uniqe_name(name))
