from mock import MagicMock
from hatak.tests.cases import ModelTestCase

from ..models import GameEntity


class GameEntityTests(ModelTestCase):
    prefix_from = GameEntity

    def setUp(self):
        super().setUp()
        self.model.borrows = [
            MagicMock(),
            MagicMock(),
            MagicMock(),
        ]
        self.model.borrows[0].is_borrowed = True
        self.model.borrows[1].is_borrowed = True
        self.model.borrows[2].is_borrowed = False

    def test_active_borrows(self):
        """active_borrows_len should return list of active borrows"""
        data = list(self.model.active_borrows())
        self.assertEqual([
            self.model.borrows[0],
            self.model.borrows[1],
        ], data)

    def test_active_borrows_len(self):
        """active_borrows_len should return lenght of active borrows."""
        self.assertEqual(2, self.model.active_borrows_len())

    def test_is_avalible(self):
        """is_avalible should return True if there is free game"""
        self.model.count = 3

        self.assertEqual(True, self.model.is_avalible())

    def test_is_avalible_false(self):
        """is_avalible should return False if there is no free game"""
        self.model.count = 2

        self.assertEqual(False, self.model.is_avalible())

    def test_move_to_box(self):
        """move_to_box should set is_in_box state to True"""
        self.model.is_in_box = False

        self.model.move_to_box()

        self.assertEqual(True, self.model.is_in_box)
