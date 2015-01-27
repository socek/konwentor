from haplugin.toster import FormTestCase, SqlFormTestCase
from haplugin.toster.fixtures import fixtures
from sqlalchemy.orm.exc import NoResultFound

from ..forms import GameAddForm, GameDeleteForm, GameEditForm
from ..models import Game


class GameAddFormTest(FormTestCase):
    prefix_from = GameAddForm

    def test_overal_validation_success(self):
        """GameAddForm should check if there is game of the same name."""
        self.add_mock_object(self.form, 'validate_uniqe_name')
        self.mocks['validate_uniqe_name'].return_value = True

        result = self.form.overal_validation({'name': ['myname']})

        self.mocks['validate_uniqe_name'].assert_called_once_with('myname')
        self.assertEqual(True, result)

    def test_overal_validation_fail(self):
        self.add_mock_object(self.form, 'validate_uniqe_name')
        self.mocks['validate_uniqe_name'].return_value = False

        result = self.form.overal_validation({'name': ['myname']})

        self.mocks['validate_uniqe_name'].assert_called_once_with('myname')
        self.assertEqual(False, result)
        self.assertEqual(
            'Gra o takiej nazwie już istnieje.', self.form.message)


class SqlGameAddFormTests(SqlFormTestCase):
    prefix_from = GameAddForm

    def test_validate_uniqe_name_found(self):
        """validate_uniqe_name should return False if name found"""
        assert self.form.validate_uniqe_name('first') is False

    def test_validate_uniqe_name_not_found(self):
        """validate_uniqe_name should return True if name not found"""
        assert self.form.validate_uniqe_name('firstasdasd') is True

    def test_submit(self):
        """GameAddForm should create new game."""
        self.form.parse_dict({
            'name': ['my dynamic name', ],
            'players_description': ['players description'],
            'time_description': ['time description'],
            'type_description': ['type description'],
            'difficulty': ['difficulty'],
        })
        self.form.on_success()

        self.db.flush()
        game = self.query(Game).filter_by(name='my dynamic name').one()
        assert 'my dynamic name' == game.name
        assert 'players description' == game.players_description
        assert 'time description' == game.time_description
        assert 'type description' == game.type_description
        assert 'difficulty' == game.difficulty

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
            self.form.set_value('obj_id', self.game.id)
            self.form.on_success()

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
                self.form.fields['name'].get_name(): [
                    'my mega name', ],
                self.form.fields['id'].get_name(): [
                    str(self.game.id), ],
                self.form.fields['players_description'].get_name(): [
                    'players description'],
                self.form.fields['time_description'].get_name(): [
                    'time description'],
                self.form.fields['type_description'].get_name(): [
                    'type description'],
                self.form.fields['difficulty'].get_name(): [
                    'difficulty'],
            })
            assert self.form.validate() is True

            self.db.flush()
            game = self.query(Game).filter_by(id=self.game.id).one()
            assert 'my mega name' == game.name
            assert 'players description' == game.players_description
            assert 'time description' == game.time_description
            assert 'type description' == game.type_description
            assert 'difficulty' == game.difficulty
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
