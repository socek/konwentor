from konwentor.game.driver import GameDriver
from haplugin.sql.testing import DriverFixture
from konwentor.game.models import Game


class TestGameDriver(DriverFixture):

    def _get_driver_class(self):
        return GameDriver

    def test_get_game_listbox_view(self, fdriver, fixtures):
        fdriver.model = Game
        room = fixtures['Convent']['first'].rooms[0]

        games = fdriver.get_game_listbox_view(room, False)
        game_ids = set([game.GameEntity.id for game in games])
        assert game_ids == set([
            fixtures['GameEntity'][0].id,
            fixtures['GameEntity'][1].id])

    def test_get_game_listbox_view_in_box(self, fdriver, fixtures):
        fdriver.model = Game
        room = fixtures['Convent']['first'].rooms[0]

        games = fdriver.get_game_listbox_view(room, True)
        game_ids = set([game.GameEntity.id for game in games])
        assert game_ids == set([
            fixtures['GameEntity'][2].id])
