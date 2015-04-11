from konwentor.application.driver import KonwentorDriver
from haplugin.sql.testing import DriverFixture
from konwentor.game.models import Game


class TestKonwentorDriver(DriverFixture):

    def _get_driver_class(self):
        return KonwentorDriver

    def test_get_objects(self, fdriver, fixtures):
        fdriver.model = Game
        games = fdriver.get_objects(id=fixtures['Game']['first'].id).all()
        assert games == [fixtures['Game']['first']]
