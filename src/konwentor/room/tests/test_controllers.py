from pytest import fixture

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
