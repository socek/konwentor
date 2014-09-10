from hatak.tests.cases import FormTestCase, SqlFormTestCase
from sqlalchemy.orm.exc import NoResultFound

from ..forms import GameAddForm, GameDeleteForm
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

        game.remove(self.db)
        self.db.commit()


class SqlGameDeleteFormTests(SqlFormTestCase):
    prefix_from = GameDeleteForm

    def test_submit(self):
        """GameDeleteForm should delete game"""
        element = Game(name='my creazy name')
        self.db.add(element)
        self.db.commit()
        _id = element.id
        del(element)

        self.form.submit({'obj_id': [_id]})

        self.db.flush()
        self.assertRaises(
            NoResultFound,
            self.query(Game).filter_by(id=_id).one)
