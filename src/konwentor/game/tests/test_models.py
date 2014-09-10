from mock import MagicMock
from hatak.tests.cases import ModelTestCase

from ..models import Game


class GameTests(ModelTestCase):
    prefix_from = Game

    def test_remove(self):
        """remove should remove the game and all it's childs"""
        removed = []

        def side_effect(obj):
            removed.append(obj)

        borrow = MagicMock()
        entity = MagicMock()
        entity.borrows = [borrow]
        copy = MagicMock()
        copy.entities = [entity]
        self.model.copies = [copy]

        self.db.delete.side_effect = side_effect

        self.model.remove(self.db)

        self.assertEqual(
            [borrow, entity, copy, self.model],
            removed)
