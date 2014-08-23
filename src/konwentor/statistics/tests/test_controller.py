from ..controller import StatisticsController
from konwentor.application.tests.case import ControllerTestCase
from konwentor.application.tests.case import SqlControllerTestCase
from konwentor.application.tests.fixtures import fixtures


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

    def test_get_borrows_empty(self):
        self.controller.data = {'convent': fixtures['Convent']['third']}
        borrows = self.controller.get_borrows()
        self.assertEqual([], borrows)

    def test_add_all_games(self):
        self.controller.data = {
            'convent': fixtures['Convent']['first'],
            'statistics': [],
            }
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
        self.controller.data = {
            'convent': fixtures['Convent']['first'],
            'statistics': [],
            }
        self.controller.add_all_copies()
        result = self.controller.data['statistics'][0]
        self.assertEqual(
            {
                'name': 'Sztuk gier',
                'value': 7,
            },
            result,
            '3 copies of the same game nad 4 copy of another makes 7 games')
