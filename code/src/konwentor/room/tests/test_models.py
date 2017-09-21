from pytest import fixture

from hatak.testing import RequestFixture

from ..models import Room


class TestGameBorrowUnit(RequestFixture):

    @fixture
    def model(self):
        return Room()

    def test_repr(self, model):
        """repr should return name of room"""
        model.id = 10
        model.name = 'my name'
        assert repr(model) == 'Room (10): my name'
