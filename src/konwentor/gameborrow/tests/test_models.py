from datetime import datetime

from haplugin.toster import TestCase

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

    def test_make_hash_document(self):
        gameborrow = GameBorrow()
        gameborrow.settings = {'personal_seed': 'abc'}
        hash1 = gameborrow.make_hash_document('document1', 'number1')
        hash2 = gameborrow.make_hash_document('document1', 'number1')
        hash3 = gameborrow.make_hash_document('document1', 'number2')
        hash4 = gameborrow.make_hash_document('document2', 'number1')

        self.assertEqual(hash1, hash2)
        self.assertNotEqual(hash2, hash3)
        self.assertNotEqual(hash2, hash4)
        self.assertNotEqual(hash3, hash4)

    def test_make_hash_document_changing_seed(self):
        gameborrow = GameBorrow()
        gameborrow.settings = {'personal_seed': 'abc'}
        hash1 = gameborrow.make_hash_document('document1', 'number1')
        gameborrow.settings = {'personal_seed': 'cba'}
        hash2 = gameborrow.make_hash_document('document1', 'number1')

        self.assertNotEqual(hash1, hash2)

    def test_set_document(self):
        gameborrow = GameBorrow()
        gameborrow.settings = {'personal_seed': 'abc'}
        hash1 = gameborrow.make_hash_document('document1', 'number1')

        gameborrow.set_document('document1', 'number1')

        self.assertEqual(hash1, gameborrow.stats_hash)
