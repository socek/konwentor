from pytest import fixture, yield_fixture, raises
from mock import MagicMock, call, patch
from pyramid.httpexceptions import HTTPNotFound

from ..controllers import ConventDelete, ChooseConventController
from ..controllers import ConventEditController
from ..controllers import ConventListController, ConventAdd
from ..controllers import EndConventController, StartConventController
from ..forms import ConventAddForm, ConventDeleteForm, ConventEditForm
from konwentor.application.testing import ControllerFixture


class LocalFixtures(ControllerFixture):

    @yield_fixture
    def verify_convent_id(self, controller):
        patcher = patch.object(controller, 'verify_convent_id', auto_spec=True)
        with patcher as mock:
            yield mock


class TestConventListController(LocalFixtures):

    @yield_fixture
    def get_convent_widgets(self, controller):
        patcher = patch.object(
            controller, 'get_convent_widgets', auto_spec=True)
        with patcher as mock:
            yield mock

    @yield_fixture
    def ConventWidget(self):
        patcher = patch('konwentor.convent.controllers.ConventWidget')
        with patcher as mock:
            yield mock

    @yield_fixture
    def get_convents(self, controller):
        patcher = patch.object(controller, 'get_convents')
        with patcher as mock:
            yield mock

    def _get_controller_class(self):
        return ConventListController

    def test_make(self, controller, get_convent_widgets, data, request):
        """
        ConventListController should create convents widgets and get actual
        selected convent_id from session
        """
        request.session = {'convent_id': 10}

        controller.make()

        assert data == {
            'choosed_id': 10,
            'convents': get_convent_widgets.return_value,
        }

    def test_get_convent_widgets(
        self,
        controller,
        get_convents,
        ConventWidget,
        request,
    ):
        """get_convent_widgets should wrap all convents with ConventWidget"""
        get_convents.return_value = ['1', ]

        result = controller.get_convent_widgets()

        assert result == [ConventWidget.return_value]

        ConventWidget.assert_called_once_with(
            self.request, '1')

    def test_get_convents(self, controller, fixtures):
        """get_convents should return all convents"""
        convents = controller.get_convents()
        for convent in convents:
            assert convent in fixtures['Convent'].values()

        # -1 in len(fixtures['Convent']) means the 1 convent which is inactive
        assert len(convents) == len(fixtures['Convent']) - 1


class TestConventAdd(LocalFixtures):

    def _get_controller_class(self):
        return ConventAdd

    def test_make_success(self, form, controller, add_form, redirect):
        """
        ConventAdd should add ConventAddForm form and redirect to
        convent:list if the form is successed
        """
        form.validate.return_value = True

        controller.make()

        add_form.assert_called_once_with(ConventAddForm)
        redirect.assert_called_once_with('convent:list')
        form.validate.assert_called_once_with()

    def test_make_fail(self, form, controller, add_form, redirect):
        """
        ConventAdd should add ConventAddForm form  and do nothing
        if the form is failed or not used
        """
        form.validate.return_value = False

        controller.make()

        add_form.assert_called_once_with(ConventAddForm)
        assert not redirect.called
        form.validate.assert_called_once_with()


class TestConventEditController(LocalFixtures):

    @fixture(autouse=True)
    def setUp(self, matchdict):
        matchdict['obj_id'] = '10'

    @yield_fixture
    def get_convent(self, controller):
        patcher = patch.object(controller, 'get_convent')
        with patcher as mock:
            yield mock

    @fixture
    def convent(self, get_convent):
        return get_convent.return_value

    def _get_controller_class(self):
        return ConventEditController

    def test_make_success(self, form, controller, add_form, redirect, convent):
        """
        ConventEdit should add ConventEditForm form and redirect to
        convent:list if the form is successed.
        """
        form.validate.return_value = True
        convent.rooms = [MagicMock(), MagicMock()]

        controller.make()

        form.validate.assert_called_once_with()
        form.set_value.assert_has_calls([
            call('id', convent.id),
            call('name', convent.name),
            call('room', convent.rooms[0].name, 0),
            call('room', convent.rooms[1].name, 1),
        ])
        add_form.assert_called_once_with(ConventEditForm)
        redirect.assert_called_once_with('convent:list')

    def test_make_fail(
        self,
        form,
        controller,
        add_form,
        redirect,
        convent,
    ):
        """
        ConventEdit should add ConventAddForm form  and do nothing if the form
        is failed or not used.
        """
        form.validate.return_value = False

        controller.make()

        form.validate.assert_called_once_with()
        form.set_value.assert_has_calls([
            call('id', convent.id),
            call('name', convent.name),
        ])

        add_form.assert_called_once_with(ConventEditForm)
        assert not redirect.called

    def test_get_convent_when_convent_exists(
        self,
        fixtures,
        matchdict,
        controller,
        data,
    ):
        convent = fixtures['Convent']['first']
        matchdict['obj_id'] = str(convent.id)

        result = controller.get_convent()

        assert convent == data['convent']
        assert convent == result

    def test_get_convent_when_convent_not_exists(
        self,
        matchdict,
        controller,
        fixtures
    ):
        matchdict['obj_id'] = '1231231231231124'

        with raises(HTTPNotFound):
            controller.get_convent()

    def test_get_convent_when_convent_is_inactive(
        self,
        matchdict,
        controller,
        fixtures
    ):
        convent = fixtures['Convent']['inactive']
        matchdict['obj_id'] = str(convent.id)

        with raises(HTTPNotFound):
            controller.get_convent()


class TestConventDelete(LocalFixtures):

    def _get_controller_class(self):
        return ConventDelete

    def test_make_success(
        self,
        controller,
        add_form,
        verify_convent_id,
        redirect,
        matchdict
    ):
        """
        .make should verify convent_id, proccess form and redirect if form was
        successed.
        """

        matchdict['obj_id'] = 'my obj id'
        form = add_form.return_value
        form.validate.return_value = True

        controller.make()

        verify_convent_id.assert_called_once_with()
        add_form.assert_called_once_with(ConventDeleteForm)
        form.validate.assert_called_once_with()
        form.set_value.assert_called_once_with(
            'obj_id', 'my obj id')
        redirect.assert_called_once_with('convent:list')

    def test_make_fail(
        self,
        controller,
        add_form,
        verify_convent_id,
        matchdict
    ):
        """make should verify convent_id, and proccess form"""
        matchdict['obj_id'] = 'my obj id'
        form = add_form.return_value
        form.validate.return_value = False

        controller.make()

        verify_convent_id.assert_called_once_with()
        add_form.assert_called_once_with(ConventDeleteForm)
        form.set_value.assert_called_once_with(
            'obj_id', 'my obj id')
        form.validate.assert_called_once_with()

    def test_verify_convent_id_success(
        self,
        controller,
        add_form,
        fixtures,
        data,
        matchdict,
    ):
        """verify_convent_id should place Convent object in .data['convent']
        when the convent_id is poiting to existing row in db."""
        matchdict['obj_id'] = fixtures['Convent']['first'].id

        controller.verify_convent_id()

        assert data['convent'] == fixtures['Convent']['first']

    def test_verify_convent_id_failed(
        self,
        controller,
        matchdict,
        fixtures
    ):
        """verify_convent_id should raise HTTPNotFound when no convent found"""
        matchdict['obj_id'] = 12331

        with raises(HTTPNotFound):
            controller.verify_convent_id()

    def test_verify_convent_id_on_not_active_convent(
        self,
        controller,
        matchdict,
        fixtures
    ):
        """
        verify_convent_id should raise HTTPNotFound when inpute id of not
        active convent.
        """
        matchdict['obj_id'] = fixtures['Convent']['inactive'].id

        with raises(HTTPNotFound):
            controller.verify_convent_id()


class TestChooseConventController(LocalFixtures):

    def _get_controller_class(self):
        return ChooseConventController

    def test_make(
        self,
        controller,
        matchdict,
        verify_convent_id,
        redirect,
        request
    ):
        """
        ChooseConventController should verify convent_id, switch selected
        convent and redirect to gamecopy:list
        """
        matchdict['obj_id'] = '10'
        request.session = {}

        controller.make()

        verify_convent_id.assert_called_once_with()
        redirect.assert_called_once_with('gamecopy:list', room_id=0)
        controller.session['convent_id'] == 10


class TestStartConventController(LocalFixtures):

    def _get_controller_class(self):
        return StartConventController

    @yield_fixture
    def switch_convent(self, controller):
        patcher = patch.object(controller, 'switch_convent')
        with patcher as mock:
            yield mock

    def test_make(
        self,
        data,
        controller,
        verify_convent_id,
        switch_convent,
        redirect,
        mdb
    ):
        """
        StartConventController should verify convent_id, switch_convent,
        start it and redirect to gamecopy:add
        """
        data['convent'] = MagicMock()

        controller.make()

        verify_convent_id.assert_called_once_with()
        switch_convent.assert_called_once_with()
        assert data['convent'].state == 'running'
        mdb.commit.assert_called_once_with()
        redirect.assert_called_once_with('gamecopy:add', room_id=0)


class TestEndConventController(LocalFixtures):

    def _get_controller_class(self):
        return EndConventController

    def test_make(
        self,
        data,
        controller,
        verify_convent_id,
        redirect,
        mdb
    ):
        """
        EndConventController should verify convent_id, end convent,
        and redirect to convent:list
        """
        data['convent'] = MagicMock()

        controller.make()

        verify_convent_id.assert_called_once_with()
        data['convent'].state == 'ended'
        mdb.commit.assert_called_once_with()
        redirect.assert_called_once_with('convent:list')
