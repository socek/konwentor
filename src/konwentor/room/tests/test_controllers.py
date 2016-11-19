from mock import MagicMock
from pytest import fixture, raises

from hatak.controller import EndController

from konwentor.application.testing import ControllerFixture
from ..controller import RoomController


class TestRoomController(ControllerFixture):

    def _get_controller_class(self):
        return RoomController

    @fixture
    def matchdict(self):
        return {
            'room_id': '123',
        }

    def test_second_filter(self, controller, data, matchdict):
        """
        .second_filter should move matchdict room_id to data
        """
        controller.second_filter()
        assert data['room_id'] == int(matchdict['room_id'])

    def test_get_room(self, controller, mdriver, matchdict):
        """
        .get_room should get room object wich id was in matchdict
        """
        matchdict['room_id'] = '10'

        assert controller.get_room() == mdriver.Room.get_by_id.return_value
        mdriver.Room.get_by_id.assert_called_once_with(10)

    def test_second_filter_when_room_id_is_zero(
        self,
        controller,
        matchdict,
        redirect
    ):
        """
        .second_filter should redirect to first room of a convent
        """
        matchdict['room_id'] = '0'
        matchdict['convent_id'] = '1'
        controller.convent = MagicMock()
        controller.convent.rooms = [MagicMock()]
        controller.convent.rooms[0].id = 10

        with raises(EndController):
            controller.second_filter()

        redirect.assert_called_once_with(
            'gamecopy:list',
            room_id=10,
            convent_id=1)
