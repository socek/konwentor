from mock import MagicMock
from pytest import fixture

from ..models import GameEntity


class TestGameEntity(object):
    prefix_from = GameEntity

    @fixture
    def model(self):
        model = GameEntity()
        model.borrows = [
            MagicMock(),
            MagicMock(),
            MagicMock(),
        ]
        model.borrows[0].is_borrowed = True
        model.borrows[1].is_borrowed = True
        model.borrows[2].is_borrowed = False
        return model

    def test_active_borrows(self, model):
        """active_borrows_len should return list of active borrows"""
        data = list(model.active_borrows())
        assert data == [
            model.borrows[0],
            model.borrows[1],
        ]

    def test_active_borrows_len(self, model):
        """active_borrows_len should return lenght of active borrows."""
        assert model.active_borrows_len() == 2

    def test_is_avalible(self, model):
        """is_avalible should return True if there is free game"""
        model.count = 3

        assert model.is_avalible() is True

    def test_is_avalible_false(self, model):
        """is_avalible should return False if there is no free game"""
        model.count = 2

        assert model.is_avalible() is False

    def test_move_to_box(self, model):
        """move_to_box should set is_in_box state to True"""
        model.is_in_box = False

        model.move_to_box()

        assert model.is_in_box is True
