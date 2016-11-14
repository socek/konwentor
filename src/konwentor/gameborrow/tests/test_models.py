from datetime import datetime
from pytest import fixture

from hatak.testing import RequestFixture

from ..models import GameBorrow


class TestGameBorrowUnit(RequestFixture):

    @fixture
    def model(self):
        return GameBorrow()

    def test_get_return_timestamp_when_no_timestamp(self, model):
        """
        get_return_timestamp should return empty string, when
        return_timestamp is None
        """
        model.return_timestamp = None
        model.get_return_timestamp() == ''

    def test_get_return_timestamp(self, model):
        """get_return_timestamp should return string represeting datetime"""
        model.return_timestamp = datetime(2014, 8, 24, 20, 43, 10)
        assert model.get_return_timestamp() == '2014-08-24 20:43:10'
