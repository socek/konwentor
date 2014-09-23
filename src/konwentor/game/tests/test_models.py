from hatak.plugins.toster.cases import ModelTestCase

from ..models import Game


class GameTests(ModelTestCase):
    prefix_from = Game
