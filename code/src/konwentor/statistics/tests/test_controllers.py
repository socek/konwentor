from pytest import fixture, yield_fixture
from mock import patch

from ..controllers import StatisticsController
from konwentor.application.testing import ControllerFixture


class TestStatisticsController(ControllerFixture):

    def _get_controller_class(self):
        return StatisticsController

    def test_add_all_borrows(self, controller):
        controller.data = {
            'statistics': [],
            'borrows': [1, 2, 3], }

        controller.add_all_borrows()

        result = controller.data['statistics'][0]
        assert result['name'] == 'Wypożyczonych gier'
        assert result['value'] == 3


class TestStatisticsSqls(ControllerFixture):

    @fixture(autouse=True)
    def setUp(self, fixtures, data):
        data['convent'] = fixtures['Convent']['first']

    def _get_controller_class(self):
        return StatisticsController

    def test_get_borrows_empty(self, controller, fixtures):
        controller.data = {'convent': fixtures['Convent']['third']}
        borrows = controller.get_borrows()
        assert borrows == []

    def test_get_borrows(self, controller, fixtures):
        controller.data = {'convent': fixtures['Convent']['second']}
        borrows = controller.get_borrows()
        assert borrows == [
            fixtures['GameBorrow'][3],
            fixtures['GameBorrow'][4]
        ]

    def test_add_all_games(self, controller, fixtures, data):
        data['convent'] = fixtures['Convent']['first']
        data['statistics'] = []
        controller.add_all_games()
        result = controller.data['statistics'][0]
        assert result == {
            'name': 'Różnych gier',
            'value': 2,
        }

    def test_add_all_copies(self, controller, fixtures, data):
        """
        3 copies of the same game nad 4 copy of another makes 7 games
        """
        data['statistics'] = []
        controller.add_all_copies()
        result = controller.data['statistics'][0]
        assert result == {
            'name': 'Sztuk gier',
            'value': 7,
        }

    def test_add_all_people(self, controller, fixtures, data):
        data['statistics'] = []
        controller.add_all_people()

        assert data['statistics'][0] == {
            'name': 'Ilość różnych osób',
            'value': 2,
        }

    def test_add_top_games(self, controller, fixtures, data):
        controller.add_top_games()

        assert data['games'] == [(2, 'first'), (1, 'second')]

    def test_add_top_people(self, controller, data):
        controller.add_top_people()

        assert data['peoples'] == [
            ('Franek Kimono', 2),
            ('Ten Drugi', 1),
        ]

    @yield_fixture
    def verify_convent(self, controller):
        with patch.object(controller, 'verify_convent') as mock:
            yield mock

    @yield_fixture
    def get_convent(self, controller):
        with patch.object(controller, 'get_convent') as mock:
            yield mock

    def test_make(
        self,
        controller,
        data,
        verify_convent,
        get_convent,
        fixtures
    ):
        verify_convent.return_value = True
        get_convent.return_value = fixtures['Convent']['first']
        controller.make()

    def test_make_verify(
        self,
        controller,
        data,
        verify_convent,
        get_convent,
        fixtures
    ):
        """
        StatisticsController should verify_convent and do nothing if it
        fails
        """
        verify_convent.return_value = False

        controller.make()

        assert not get_convent.called
