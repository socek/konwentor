from haplugin.toster import ControllerTestCase, SqlControllerTestCase
from haplugin.toster.fixtures import fixtures

from ..controllers import StatisticsController


class StatisticsControllerTest(ControllerTestCase):

    prefix_from = StatisticsController

    def test_add_all_borrows(self):
        self.controller.data = {
            'statistics': [],
            'borrows': [1, 2, 3], }

        self.controller.add_all_borrows()

        result = self.controller.data['statistics'][0]
        self.assertEqual('Wypożyczonych gier', result['name'])
        self.assertEqual(3, result['value'])


class StatisticsSqlsTest(SqlControllerTestCase):

    prefix_from = StatisticsController

    def setUp(self):
        super().setUp()
        self.data['statistics'] = []
        self.data['convent'] = fixtures['Convent']['first']

    def test_get_borrows_empty(self):
        self.controller.data = {'convent': fixtures['Convent']['third']}
        borrows = self.controller.get_borrows()
        self.assertEqual([], borrows)

    def test_add_all_games(self):
        self.controller.add_all_games()
        result = self.controller.data['statistics'][0]
        self.assertEqual(
            {
                'name': 'Różnych gier',
                'value': 2,
            },
            result,
            '3 copies of the same game nad 4 copy of another makes 2 '
            'uniqe games')

    def test_add_all_copies(self):
        self.controller.add_all_copies()
        result = self.controller.data['statistics'][0]
        self.assertEqual(
            {
                'name': 'Sztuk gier',
                'value': 7,
            },
            result,
            '3 copies of the same game nad 4 copy of another makes 7 games')

    def test_add_all_people(self):
        self.controller.add_all_people()

        self.assertEqual(
            {
                'name': 'Ilość różnych osób',
                'value': 2,
            },
            self.data['statistics'][0])

    def test_add_top_games(self):
        self.controller.add_top_games()

        self.assertEqual(
            [(2, 'first'), (1, 'second')], self.data['games'])

    def test_add_top_people(self):
        self.controller.add_top_people()

        self.assertEqual(
            [
                ('Franek', 'Kimono', 'paszport', '123', 2),
                ('Ten', 'Drugi', 'paszport', '1234', 1),
            ],
            self.data['peoples'])

    def test_make(self):
        self.add_mock_object(self.controller, 'verify_convent')
        self.add_mock_object(self.controller, 'get_convent')
        self.mocks['verify_convent'].return_value = True
        self.mocks['get_convent'].return_value = fixtures['Convent']['first']
        self.controller.make()

    def test_make_verify(self):
        """StatisticsController should verify_convent and do nothing if it
        fails"""
        self.add_mock_object(self.controller, 'verify_convent')
        self.add_mock_object(self.controller, 'get_convent')
        self.mocks['verify_convent'].return_value = False

        self.controller.make()

        self.assertEqual(0, self.mocks['get_convent'].call_count)
