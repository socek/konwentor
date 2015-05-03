from mock import patch
from pytest import raises, yield_fixture, mark
from sqlalchemy.orm.exc import NoResultFound

from ..forms import GameAddForm, GameDeleteForm, GameEditForm
from ..models import Game
from konwentor.application.testing import FormFixture


class LocalFixtures(FormFixture):

    @yield_fixture
    def validate_uniqe_name(self, form):
        patcher = patch.object(form, 'validate_uniqe_name')
        with patcher as mock:
            yield mock


class TestGameAddForm(LocalFixtures):

    def _get_form_class(self):
        return GameAddForm

    def test_overal_validation_success(self, validate_uniqe_name, form):
        """GameAddForm should check if there is game of the same name."""
        validate_uniqe_name.return_value = True

        result = form.overal_validation({'name': ['myname']})

        validate_uniqe_name.assert_called_once_with('myname')
        assert result is True

    def test_overal_validation_fail(self, validate_uniqe_name, form):
        validate_uniqe_name.return_value = False

        result = form.overal_validation({'name': ['myname']})

        validate_uniqe_name.assert_called_once_with('myname')
        assert result is False
        assert form.message == 'Gra o takiej nazwie już istnieje.'

    def test_validate_uniqe_name_found(self, form, fixtures):
        """validate_uniqe_name should return False if name found"""
        assert form.validate_uniqe_name('first') is False

    def test_validate_uniqe_name_not_found(self, form, fixtures):
        """validate_uniqe_name should return True if name not found"""
        assert form.validate_uniqe_name('firstasdasd') is True

    def test_submit(self, form, fixtures, db):
        """GameAddForm should create new game."""
        form.parse_dict({
            'name': ['my dynamic name', ],
            'players_description': ['players description'],
            'time_description': ['time description'],
            'type_description': ['type description'],
            'difficulty': ['difficulty'],
        })
        form.on_success()

        db.flush()
        game = db.query(Game).filter_by(name='my dynamic name').one()
        assert 'my dynamic name' == game.name
        assert 'players description' == game.players_description
        assert 'time description' == game.time_description
        assert 'type description' == game.type_description
        assert 'difficulty' == game.difficulty

        db.delete(game)
        db.commit()


class GameFactoryMixin(object):

    def create_game(self, db, name='my creazy name'):
        self.game = Game(name='my creazy name')
        db.add(self.game)
        db.commit()
        return self.game.id

    def delete_game(self, db):
        self.driver.Game.delete(self.game)


class TestGameDeleteForm(LocalFixtures, GameFactoryMixin):

    def _get_form_class(self):
        return GameDeleteForm

    def test_submit(self, db, form, driver):
        """GameDeleteForm should delete game"""
        self.create_game(db)

        try:
            form.set_value('obj_id', self.game.id)
            form.on_success()

            db.flush()
            with raises(NoResultFound):
                driver.Game.get_active(self.game.id)
        finally:
            self.delete_game(db)


class TestGameEditForm(LocalFixtures, GameFactoryMixin):

    def _get_form_class(self):
        return GameEditForm

    @mark.usefixtures('CsrfMustMatch')
    def test_submit(self, db, driver, form, postdata):
        self.create_game(db)
        try:
            postdata[form.fields['name'].get_name()] = ['my mega name', ]
            postdata[form.fields['id'].get_name()] = [str(self.game.id), ]
            postdata[form.fields['players_description'].get_name()] = [
                'players description']
            postdata[form.fields['time_description'].get_name()] = [
                'time description']
            postdata[form.fields['type_description'].get_name()] = [
                'type description']
            postdata[form.fields['difficulty'].get_name()] = [
                'difficulty']

            assert form.validate() is True

            db.flush()
            game = db.query(Game).filter_by(id=self.game.id).one()
            assert 'my mega name' == game.name
            assert 'players description' == game.players_description
            assert 'time description' == game.time_description
            assert 'type description' == game.type_description
            assert 'difficulty' == game.difficulty
        finally:
            self.delete_game(db)

    def test_validate_uniqe_name_when_name_found(self, form, fixtures):
        """validate_uniqe_name should return False if name is in database"""
        name = 'second'
        form.model = fixtures['Game']['first']
        assert form.validate_uniqe_name(name) is False

    def test_validate_uniqe_name_when_name_not_found(self, form, fixtures):
        """validate_uniqe_name should return True if name is not in database"""
        name = 'New name'
        form.model = fixtures['Game']['first']
        assert form.validate_uniqe_name(name) is True

    def test_validate_uniqe_name_when_name_not_changed(self, form, fixtures):
        """validate_uniqe_name should return True if name is in database but
        has the same id as our model"""
        name = 'first'
        form.model = fixtures['Game']['first']
        assert form.validate_uniqe_name(name) is True
