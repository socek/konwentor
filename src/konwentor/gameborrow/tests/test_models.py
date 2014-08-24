from datetime import datetime

from konwentor.application.tests.case import TestCase
from ..models import GameBorrow


class GameBorrowUnitTestCase(TestCase):

    prefix_from = GameBorrow

    def test_get_return_timestamp_when_no_timestamp(self):
        """get_return_timestamp should return empty string, when
        return_timestamp is None"""
        gameborrow = GameBorrow()
        gameborrow.return_timestamp = None
        self.assertEqual('', gameborrow.get_return_timestamp())

    def test_get_return_timestamp(self):
        """get_return_timestamp should return string represeting datetime"""
        gameborrow = GameBorrow()
        gameborrow.return_timestamp = datetime(2014, 8, 24, 20, 43, 10)
        self.assertEqual(
            '2014-08-24 20:43:10',
            gameborrow.get_return_timestamp())
