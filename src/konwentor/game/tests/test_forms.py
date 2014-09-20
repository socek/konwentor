from hatak.tests.cases import FormTestCase, SqlFormTestCase
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
        self.form.submit({'name': ['my dynamic name']})

        self.db.flush()
        game = self.query(Game).filter_by(name='my dynamic name').one()
        self.assertEqual('my dynamic name', game.name)

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
            })
            self.assertEqual(True, self.form({'id': [str(self.game.id)]}))

            self.db.flush()
            game = self.query(Game).filter_by(id=self.game.id).one()
            self.assertEqual('my mega name', game.name)
        finally:
            self.delete_game()
