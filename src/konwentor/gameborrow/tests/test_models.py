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

    def test_make_hash_document(self, model):
        model.settings = {'personal_seed': 'abc'}
        hash1 = model.make_hash_document('document1', 'number1')
        hash2 = model.make_hash_document('document1', 'number1')
        hash3 = model.make_hash_document('document1', 'number2')
        hash4 = model.make_hash_document('document2', 'number1')

        assert hash1 == hash2
        assert hash2 != hash3
        assert hash2 != hash4
        assert hash3 != hash4

    def test_make_hash_document_changing_seed(self, model):
        model.settings = {'personal_seed': 'abc'}
        hash1 = model.make_hash_document('document1', 'number1')
        model.settings = {'personal_seed': 'cba'}
        hash2 = model.make_hash_document('document1', 'number1')

        assert hash1 != hash2

    def test_set_document(self, model):
        model.settings = {'personal_seed': 'abc'}
        hash1 = model.make_hash_document('document1', 'number1')

        model.set_document('document1', 'number1')

        assert model.stats_hash == hash1
