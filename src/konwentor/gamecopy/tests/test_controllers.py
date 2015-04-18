from pytest import fixture, yield_fixture, raises
from mock import MagicMock, call, patch
from sqlalchemy.orm.exc import NoResultFound


from ..controllers import EndController
from ..controllers import GameCopyAddController, GameCopyToBoxController
from ..controllers import GameCopyControllerBase, GameCopyListController
from konwentor.gameborrow.sidemenu import SideMenuWidget
from konwentor.convent.helpers import ConventWidget
from konwentor.gamecopy.forms import GameCopyAddForm
from konwentor.application.testing import ControllerFixture


class LocalFixtures(ControllerFixture):

    @fixture
    def add_flashmsg(self, request):
        return request.add_flashmsg

    @fixture
    def session(self, request):
        request.session = {}
        return request.session

    @yield_fixture
    def verify_convent(self, controller):
        with patch.object(controller, 'verify_convent') as mock:
            mock.return_value = True
            yield mock

    @yield_fixture
    def get_convent(self, controller):
        with patch.object(controller, 'get_convent', autospec=True) as mock:
            yield mock


class TestGameCopyControllerBase(LocalFixtures):

    def _get_controller_class(self):
        return GameCopyControllerBase

    @yield_fixture
    def add_helper(self, controller):
        with patch.object(controller, 'add_helper', autospec=True) as mock:
            yield mock

    def test_verify_convent_false(
        self,
        controller,
        add_flashmsg,
        redirect,
        session
    ):
        """
        verify_convent should return False when convent_id is not in
        session
        """
        assert controller.verify_convent() is False
        add_flashmsg.assert_called_once_with(
            'Proszę wybrać konwent.', 'danger')
        redirect.assert_called_once_with('convent:list')

    def test_verify_convent_true(self, controller, session):
        """verify_convent should return True when convent_id is in session"""
        session['convent_id'] = 1

        assert controller.verify_convent() is True

    def test_make_helpers(self, controller, add_helper, get_convent):
        """make_helpers should add ConventWidget helper"""
        controller.make_helpers()

        add_helper.assert_has_calls([
            call(
                'convent',
                ConventWidget,
                get_convent.return_value,
            ),
            call(
                'sidemenu',
                SideMenuWidget,
                None,
            )
        ])


class TestGameCopyControllerBaseSql(LocalFixtures):

    def _get_controller_class(self):
        return GameCopyControllerBase

    def test_get_convent(self, controller, fixtures, session):
        """get_convent should return convent which id is saved in session."""
        convent = fixtures['Convent']['first']
        session['convent_id'] = convent.id,

        assert controller.get_convent() == convent

    def test_get_convent_on_inactive_convent(
        self,
        add_flashmsg,
        redirect,
        fixtures,
        session,
        controller
    ):
        """get_convent should raise NoResultFound when convent is inactive"""

        convent = fixtures['Convent']['inactive']
        session['convent_id'] = convent.id,

        with raises(EndController):
            controller.get_convent()

        add_flashmsg.assert_called_once_with(
            'Proszę wybrać konwent.', 'danger')
        redirect.assert_called_once_with('convent:list')


class TestGameCopyAddController(LocalFixtures):

    def _get_controller_class(self):
        return GameCopyAddController

    def test_verify_convent(self, verify_convent, controller, add_form):
        """Controller should do nothing if verify_convent fails"""
        verify_convent.return_value = False

        controller.make()

        verify_convent.assert_called_once_with()
        assert not add_form.called

    def test_form_not_submitted(
        self,
        add_form,
        controller,
        add_flashmsg,
        verify_convent
    ):
        """Controller should create form after verify_convent check."""
        form = add_form.return_value
        form.validate.return_value = None

        controller.make()

        add_form.assert_called_once_with(GameCopyAddForm)
        form.validate.assert_called_once_with()
        form.parse_dict({
            'count': 1,
            'user_id': self.user.id,
            'convent_id': self.session['convent_id'],
        })
        assert not add_flashmsg.called

    def test_form_submitted(self, controller, session, add_form, add_flashmsg):
        session['last_convent_id'] = 1
        session['last_user_id'] = -1
        session['convent_id'] = 2
        form = add_form.return_value
        form.validate.return_value = True

        controller.make()

        add_form.assert_called_once_with(GameCopyAddForm)
        form.validate.assert_called_once_with()
        form.parse_dict.assert_called_once_with({
            'count': 1,
            'user_id': -1,
            'convent_id': 1,
        })

        add_flashmsg.assert_called_once_with(
            'Dodano grę.', 'info')

        form.get_value.assert_has_calls([
            call('convent_id'),
            call('user_id'),
        ])
        assert session['last_convent_id'] == form.get_value.return_value
        assert session['last_user_id'] == form.get_value.return_value


class TestGameCopyListController(LocalFixtures):

    @fixture
    def game(self):
        return MagicMock()

    @yield_fixture
    def get_games(self, controller, game):
        patcher = patch.object(controller, 'get_games', return_value=[game])
        with patcher as mock:
            yield mock

    @yield_fixture
    def GameEntityWidget(self):
        with patch('konwentor.gamecopy.controllers.GameEntityWidget') as mock:
            yield mock

    def _get_controller_class(self):
        return GameCopyListController

    def test_get_games(self, fixtures, controller):
        """get_games should return list of games avalible on convent"""
        convent = fixtures['Convent']['first']
        result = controller.get_games(convent)

        assert len(result) == 3
        for element in result:
            assert element.GameEntity.convent == convent

    def test_verify_convent(self, verify_convent, controller, data):
        """Controller should do nothing if verify_convent fails"""
        verify_convent.return_value = False

        controller.make()

        verify_convent.assert_called_once_with()
        assert data == {}

    def test_normal(
        self,
        verify_convent,
        controller,
        get_convent,
        GameEntityWidget,
        data,
        request,
        game,
        get_games
    ):
        controller.make()

        verify_convent.assert_called_once_with()
        assert data == {
            'convent': get_convent.return_value,
            'games': [GameEntityWidget.return_value],
        }
        get_games.assert_called_once_with(get_convent.return_value)
        GameEntityWidget.assert_called_once_with(request, game)


class TestGameCopyToBoxController(LocalFixtures):

    def _get_controller_class(self):
        return GameCopyToBoxController

    @yield_fixture
    def move_to_box(self, controller):
        with patch.object(controller, 'move_to_box') as mock:
            yield mock

    @yield_fixture
    def get_game_entity(self, controller):
        with patch.object(controller, 'get_game_entity') as mock:
            yield mock

    def test_make_bad_convent_id(
        self,
        controller,
        verify_convent,
        add_flashmsg,
        redirect
    ):
        """
        GameCopyToBoxController should verify convent and do nothing if it
        fails.
        """
        verify_convent.return_value = False

        controller.make()

        verify_convent.assert_called_once_with()
        assert not add_flashmsg.called
        assert not redirect.called

    def test_make(
        self,
        controller,
        verify_convent,
        add_flashmsg,
        redirect,
        move_to_box
    ):
        """
        GameCopyToBoxController should verify convent, move game copy to box
        and redirect to gamecopy:list
        """
        verify_convent.return_value = True

        controller.make()

        verify_convent.assert_called_once_with()

        move_to_box.assert_called_once_with()
        add_flashmsg.assert_called_once_with(
            'Gra została schowana.', 'success')
        redirect.assert_called_once_with('gamecopy:list')

    def test_move_to_box(
        self,
        controller,
        verify_convent,
        add_flashmsg,
        redirect,
        get_game_entity,
        get_convent
    ):
        """move_to_box should get entity, move it to box and commit to db."""
        controller.move_to_box()

        get_convent.assert_called_once_with()
        convent = get_convent.return_value
        get_game_entity.assert_called_once_with(convent)
        entity = get_game_entity.return_value
        entity.move_to_box.assert_called_once_with()
        self.db.commit.assert_called_once_with()

    def test_get_game_entity(self, fixtures, controller):
        """
        get_game_entity should return return GameEntity which id is provided
        by matchdict and convent do match.
        """
        entity = fixtures['GameEntity'][0]
        convent = entity.convent
        self.matchdict['obj_id'] = entity.id

        assert controller.get_game_entity(convent) == entity

    def test_game_entity_when_convent_does_not_match(
        self,
        fixtures,
        controller
    ):
        """get_game_entity should raises () when convent does not match"""
        entity = fixtures['GameEntity'][0]
        convent = fixtures['Convent']['second']
        self.matchdict['obj_id'] = entity.id

        with raises(NoResultFound):
            controller.get_game_entity(convent)
