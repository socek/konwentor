from mock import MagicMock, call, patch
from pyramid.httpexceptions import HTTPNotFound
from pytest import fixture, yield_fixture, raises

from ..controllers import GameBorrowAddController, GameBorrowListController
from ..controllers import GameBorrowReturnController, ShowPersonHint
from konwentor.application.init import main
from konwentor.application.testing import ControllerFixture
from konwentor.gameborrow.models import make_hash_document
from konwentor.gameborrow.sidemenu import SideMenuWidget


class LocalFixtures(ControllerFixture):

    @yield_fixture
    def get_game_entity(self, controller):
        patcher = patch.object(controller, 'get_game_entity', autospec=True)
        with patcher as mock:
            yield mock

    @yield_fixture
    def add_flashmsg(self, request):
        patcher = patch.object(request, 'add_flashmsg', autospec=True)
        with patcher as mock:
            yield mock

    @yield_fixture
    def verify_convent(self, controller):
        patcher = patch.object(controller, 'verify_convent', autospec=True)
        with patcher as mock:
            yield mock

    @yield_fixture
    def get_convent(self, controller):
        patcher = patch.object(controller, 'get_convent', autospec=True)
        with patcher as mock:
            yield mock

    @yield_fixture
    def get_borrows(self, controller):
        patcher = patch.object(controller, 'get_borrows', autospec=True)
        with patcher as mock:
            yield mock

    @yield_fixture
    def generate_log(self, controller):
        patcher = patch.object(controller, 'generate_log', autospec=True)
        with patcher as mock:
            yield mock

    @yield_fixture
    def _on_form_success(self, controller):
        patcher = patch.object(controller, '_on_form_success', autospec=True)
        with patcher as mock:
            yield mock

    @yield_fixture
    def _on_form_fail(self, controller):
        patcher = patch.object(controller, '_on_form_fail', autospec=True)
        with patcher as mock:
            yield mock

    @yield_fixture
    def get_borrow(self, controller):
        patcher = patch.object(controller, 'get_borrow', autospec=True)
        with patcher as mock:
            yield mock

    @yield_fixture
    def return_game(self, controller):
        patcher = patch.object(controller, 'return_game', autospec=True)
        with patcher as mock:
            yield mock

    @yield_fixture
    def get_hint(self, controller):
        patcher = patch.object(controller, 'get_hint', autospec=True)
        with patcher as mock:
            yield mock

    @yield_fixture
    def get_values_by_document_and_number(self, controller):
        patcher = patch.object(
            controller, 'get_values_by_document_and_number', autospec=True)
        with patcher as mock:
            yield mock

    @yield_fixture
    def get_game_borrow_by_stat_hash(self, controller):
        patcher = patch.object(
            controller, 'get_game_borrow_by_stat_hash', autospec=True)
        with patcher as mock:
            yield mock

    @yield_fixture
    def GameBorrowReturnForm(self):
        patcher = patch(
            'konwentor.gameborrow.controllers.GameBorrowReturnForm')
        with patcher as mock:
            yield mock

    @yield_fixture
    def FormWidget(self):
        patcher = patch('konwentor.gameborrow.controllers.FormWidget')
        with patcher as mock:
            yield mock

    @yield_fixture
    def KonwentorMessage(self):
        patcher = patch('konwentor.gameborrow.controllers.KonwentorMessage')
        with patcher as mock:
            yield mock

    @yield_fixture
    def datetime(self):
        patcher = patch('konwentor.gameborrow.controllers.datetime')
        with patcher as mock:
            yield mock

    @yield_fixture
    def make_hash_document(self):
        patcher = patch('konwentor.gameborrow.controllers.make_hash_document')
        with patcher as mock:
            yield mock

    @fixture
    def form(self, add_form):
        return add_form.return_value


class TestGameBorrowAddController(LocalFixtures):

    def _get_controller_class(self):
        return GameBorrowAddController

    def test_make(
        self,
        form,
        controller,
        data,
        add_flashmsg,
        redirect,
        get_game_entity
    ):
        form.validate.return_value = False

        controller.make()

        assert data['game_entity'] == get_game_entity.return_value
        form.set_value.assert_called_once_with(
            'game_entity_id',
            data['game_entity'].id)
        form.validate.assert_called_once_with()
        assert not add_flashmsg.called
        assert not redirect.called

    def test_make_on_form(
        self,
        form,
        controller,
        data,
        add_flashmsg,
        redirect,
        get_game_entity,
        matchdict,
    ):
        form.validate.return_value = True
        matchdict['room_id'] = '10'

        controller.make()

        assert data['game_entity'] == get_game_entity.return_value
        form.set_value.assert_called_once_with(
            'game_entity_id',
            data['game_entity'].id)
        form.validate.assert_called_once_with()
        add_flashmsg.assert_called_once_with(
            'Gra została wypożyczona.', 'success')
        redirect.assert_called_once_with('gamecopy:list', room_id=10)

    def test_get_game_entity(self, controller, matchdict, fixtures):
        """get_game_entity should return GameEntity with id get from
        matchdict['obj_id']"""
        matchdict['obj_id'] = fixtures['GameEntity'][0].id

        entity = controller.get_game_entity()

        assert entity == fixtures['GameEntity'][0]

    def test_get_game_entity_not_found(self, controller, matchdict, fixtures):
        """
        get_game_entity should raise HTTPNotFound when no GameEntity found
        """
        matchdict['obj_id'] = 21321312

        with raises(HTTPNotFound):
            controller.get_game_entity()

    def test_make_helpers(self, controller, add_helper):
        """
        .make_helpers should add SideMenuWidget helper
        """
        controller.make_helpers()
        add_helper.assert_called_once_with('sidemenu', SideMenuWidget, None)


class TestGameBorrowListController(LocalFixtures):

    def _get_controller_class(self):
        return GameBorrowListController

    def test_make_no_convent(
        self,
        controller,
        verify_convent,
        get_convent,
        get_borrows,
        generate_log,
    ):
        """GameBorrowListController should do nothing when no convent found"""
        verify_convent.return_value = False

        controller.make()

        verify_convent.assert_called_once_with()
        assert not get_convent.called
        assert not get_borrows.called
        assert not generate_log.called

    def test_make(
        self,
        controller,
        verify_convent,
        get_convent,
        get_borrows,
        generate_log,
        data,
        session,
    ):
        session['convent_id'] = 123
        verify_convent.return_value = True

        controller.make()

        verify_convent.assert_called_once_with()
        get_convent.assert_called_once_with()
        get_borrows.assert_called_once_with(data['convent'])
        generate_log.assert_called_once_with(
            data['convent'])

        assert data['convent'] == get_convent.return_value
        assert data['borrows'] == get_borrows.return_value
        assert data['logs'] == generate_log.return_value

    def test_prepere_template(
        self,
        GameBorrowReturnForm,
        get_borrows,
        controller,
        get_convent,
        generate_log,
        data,
        request,
        session,
    ):
        session['convent_id'] = 123
        form = GameBorrowReturnForm.return_value
        borrow = MagicMock()
        get_borrows.return_value = [borrow]

        controller.prepere_template()

        get_convent.assert_called_once_with()
        get_borrows.assert_called_once_with(data['convent'])
        generate_log.assert_called_once_with(data['convent'])

        assert data['convent'] == get_convent.return_value
        assert data['borrows'] == get_borrows.return_value
        assert data['logs'] == generate_log.return_value

        GameBorrowReturnForm.assert_called_once_with(request)
        form.set_value.assert_has_calls([
            call('game_borrow_id', borrow.id),
            call('convent_id', session['convent_id']),
        ])

    def test_process_form_on_empty(
        self,
        GameBorrowReturnForm,
        get_borrows,
        controller,
        get_convent,
        generate_log,
        data,
        request,
        _on_form_fail,
        _on_form_success,
        session,
    ):
        session['convent_id'] = 1234
        form = GameBorrowReturnForm.return_value
        form.success = form.validate.return_value = None

        controller.process_form()

        GameBorrowReturnForm.assert_called_once_with(
            request)
        form.set_value.assert_called_once_with(
            'convent_id', session['convent_id'])
        form.validate.assert_called_once_with()

        assert not _on_form_success.called
        assert not _on_form_fail.called

    def test_process_form_on_success(
        self,
        GameBorrowReturnForm,
        get_borrows,
        controller,
        get_convent,
        generate_log,
        data,
        request,
        _on_form_fail,
        _on_form_success,
        session,
    ):
        session['convent_id'] = 1234
        form = GameBorrowReturnForm.return_value
        form.success = form.validate.return_value = True

        controller.process_form()

        GameBorrowReturnForm.assert_called_once_with(
            request)
        form.set_value.assert_called_once_with(
            'convent_id', session['convent_id'])
        form.validate.assert_called_once_with()

        _on_form_success.assert_called_once_with(form)
        assert not _on_form_fail.called

    def test_process_form_on_fail(
        self,
        GameBorrowReturnForm,
        get_borrows,
        controller,
        get_convent,
        generate_log,
        data,
        request,
        _on_form_fail,
        _on_form_success,
        session
    ):
        session['convent_id'] = '12345'
        form = GameBorrowReturnForm.return_value
        form.success = form.validate.return_value = False

        controller.process_form()

        GameBorrowReturnForm.assert_called_once_with(
            request)
        form.set_value.assert_called_once_with(
            'convent_id', session['convent_id'])
        form.validate.assert_called_once_with()

        assert not _on_form_success.called
        _on_form_fail.assert_called_once_with(form)

    def test_on_form_fail_with_form_message(
        self,
        controller,
    ):
        form = MagicMock()
        game_entity_id = MagicMock()
        form.fields = {'game_entity_id': game_entity_id}
        msg = MagicMock()
        form.messages = [msg]

        controller._on_form_fail(form)

        msg.assert_called_once_with()
        self.add_flashmsg(
            msg.return_value,
            'danger')

    def test_on_form_fail_with_value_message(
        self,
        controller,
        add_flashmsg,
    ):
        form = MagicMock()
        game_entity_id = MagicMock()
        form.fields = {'game_entity_id': game_entity_id}
        game_entity_id.get_value_errors.return_value = ['str']

        form.messages = []

        controller._on_form_fail(form)

        game_entity_id.get_value_errors.assert_called_once_with()

        add_flashmsg.assert_called_once_with(
            'str',
            'danger')

    def test_on_form_success_with_empty_game_entity_id(
        self,
        controller,
        add_flashmsg,
        redirect,
    ):
        game_entity_id = MagicMock()
        form = MagicMock()
        form.fields = {
            'game_entity_id': game_entity_id,
        }
        game_entity_id.get_value.return_value = False
        form.borrow.gameentity.gamecopy.game.name = 'first'

        controller._on_form_success(form)

        game_entity_id.get_value.assert_called_once_with(default=False)

        message = 'Gra "first" została zwrócona.'
        add_flashmsg.assert_called_once_with(message, 'info')
        redirect.assert_called_once_with('gameborrow:list', True)

    def test_on_form_success_with_game_entity_id(
        self,
        controller,
        add_flashmsg,
        redirect,
    ):
        game_entity_id = MagicMock()
        form = MagicMock()
        form.fields = {
            'game_entity_id': game_entity_id,
        }
        game_entity_id.get_value.return_value = True
        form.borrow.gameentity.gamecopy.game.name = 'first'
        form.new_borrow.gameentity.gamecopy.game.name = 'second'

        controller._on_form_success(form)

        game_entity_id.get_value.assert_called_once_with(default=False)

        message = ('Gra "first" została zwrócona, a "second" została'
                   ' pożyczona.')
        add_flashmsg.assert_called_once_with(message, 'info')
        redirect.assert_called_once_with('gameborrow:list', True)

    def test_get_borrows(
        self,
        controller,
        fixtures,
        matchdict,
    ):
        """get_borrows should return all active borrows"""
        matchdict['room_id'] = fixtures['Convent']['first'].rooms[0].id
        entities = controller.get_borrows(fixtures['Convent']['first'])
        assert entities == [
            fixtures['GameBorrow'][0],
            fixtures['GameBorrow'][1]
        ]

    def test_generate_log(
        self,
        controller,
        fixtures,
        matchdict,
    ):
        """generate_log should return all non active borrows"""
        matchdict['room_id'] = fixtures['Convent']['first'].rooms[0].id
        entities = controller.generate_log(fixtures['Convent']['first'])
        assert entities == [fixtures['GameBorrow'][2]]


class TestGameBorrowReturnController(LocalFixtures):

    @fixture
    def borrow(self, get_borrow):
        return get_borrow.return_value

    def _get_controller_class(self):
        return GameBorrowReturnController

    def test_make(
        self,
        return_game,
        borrow,
        controller,
        add_flashmsg,
        redirect,
    ):
        """
        GameBorrowReturnController should set status of GameBorrow to
        "returned".
        """
        return_game.return_value = True
        borrow.is_borrowed = True

        controller.make()

        return_game.assert_called_once_with(borrow)
        add_flashmsg.assert_called_once_with(
            'Gra została oddana.', 'success')
        redirect.assert_called_once_with('gameborrow:list')

    def test_make_when_already_returned(
        self,
        controller,
        return_game,
        borrow,
        add_flashmsg,
        redirect,
    ):
        """
        GameBorrowReturnController should do nothing if GameBorrow is
        already returned.
        """
        return_game.return_value = True
        borrow.is_borrowed = False

        controller.make()

        assert not return_game.called
        add_flashmsg.assert_called_once_with(
            'Gra została oddana wcześniej.', 'warning')
        redirect.assert_called_once_with('gameborrow:list')

    def test_return_game(
        self,
        controller,
        borrow,
        datetime,
        mdb,
    ):
        """
        return_game should set is_borrowed state to False and set timestamp
        """

        controller.return_game(borrow)

        assert not borrow.is_borrowed
        assert borrow.return_timestamp == datetime.utcnow.return_value
        mdb.commit.assert_called_once_with()

    def test_get_borrow(
        self,
        controller,
        fixtures,
        matchdict,
    ):
        """
        get_borrow should return GameBorrow with id get from
        matchdict['obj_id']
        """
        matchdict['obj_id'] = fixtures['GameBorrow'][0].id

        entity = controller.get_borrow()

        assert entity == fixtures['GameBorrow'][0]

    def test_get_borrow_not_found(self, matchdict, controller, fixtures):
        """
        get_borrow should raise HTTPNotFound when no GameBorrow found
        """
        matchdict['obj_id'] = 21321312

        with raises(HTTPNotFound):
            controller.get_borrow()


class TestsShowPersonHint(LocalFixtures):

    def _get_controller_class(self):
        return ShowPersonHint

    def test_make(
        self,
        controller,
        data,
        get_hint,
        request,
    ):
        request.POST = {'number': 'something'}

        controller.make()

        get_hint.assert_called_once_with('something')
        obj = get_hint.return_value
        assert data == {
            'name': obj.name,
            'surname': obj.surname,
            'document': obj.document,
        }

    def test_get_hint_found(
        self,
        controller,
        get_values_by_document_and_number,
    ):
        controller.document_types = ['one']

        result = controller.get_hint('something')

        mocked = get_values_by_document_and_number
        assert result == mocked.return_value
        mocked.assert_called_once_with('one', 'something')

    def test_get_hint_not_found(
        self,
        controller,
        get_values_by_document_and_number,
    ):
        controller.document_types = ['one']
        get_values_by_document_and_number.side_effect = AttributeError

        result = controller.get_hint('something')

        assert result.name == ''
        assert result.surname == ''
        assert result.document == ''
        get_values_by_document_and_number.assert_called_once_with(
            'one', 'something')

    def test_get_values_by_document_and_number(
        self,
        controller,
        get_game_borrow_by_stat_hash,
        fixtures,
        make_hash_document,
    ):
        controller.request = MagicMock()
        controller.request = MagicMock()

        result = controller.get_values_by_document_and_number(
            'doc',
            'num')

        assert result == get_game_borrow_by_stat_hash.return_value

        assert result.document == 'doc'

        make_hash_document.assert_called_once_with(
            controller.request,
            'doc',
            'num')

    def test_get_values_by_document_and_number_raise_attribute_error(
        self,
        controller,
        get_game_borrow_by_stat_hash,
        make_hash_document,
    ):
        controller.request = MagicMock()
        get_game_borrow_by_stat_hash.return_value = None

        with raises(AttributeError):
            controller.get_values_by_document_and_number('doc', 'num')

        make_hash_document.assert_called_once_with(
            controller.request,
            'doc',
            'num')

    def test_get_game_borrow_by_stat_hash(
        self,
        controller,
        request,
        fixtures,
    ):
        request.registry['settings'] = main.settings
        hashed = make_hash_document(controller.request, 'paszport', '123')

        result = controller.get_game_borrow_by_stat_hash(hashed)

        assert result.name == 'FranekLast'
        assert result.surname == 'KimonoLast'
