from hatak.testing import ControllerFixture
from haplugin.sql.testing import DatabaseFixture

from ..controllers import StatisticsController


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


class TestStatisticsSqls(ControllerFixture, DatabaseFixture):

    def _get_controller_class(self):
        return StatisticsController

    def test_get_borrows_empty(self, controller, fixtures):
        controller.data = {'convent': fixtures['Convent']['third']}
        borrows = controller.get_borrows()
        assert borrows == []

#     def test_get_borrows(self):
#         self.controller.data = {'convent': fixtures['Convent']['second']}
#         borrows = self.controller.get_borrows()
#         self.assertEqual(
#             [
#                 fixtures['GameBorrow'][3],
#                 fixtures['GameBorrow'][4]],
#             borrows)

#     def test_add_all_games(self):
#         self.controller.add_all_games()
#         result = self.controller.data['statistics'][0]
#         self.assertEqual(
#             {
#                 'name': 'Różnych gier',
#                 'value': 2,
#             },
#             result,
#             '3 copies of the same game nad 4 copy of another makes 2 '
#             'uniqe games')

#     def test_add_all_copies(self):
#         self.controller.add_all_copies()
#         result = self.controller.data['statistics'][0]
#         self.assertEqual(
#             {
#                 'name': 'Sztuk gier',
#                 'value': 7,
#             },
#             result,
#             '3 copies of the same game nad 4 copy of another makes 7 games')

#     def test_add_all_people(self):
#         self.controller.add_all_people()

#         self.assertEqual(
#             {
#                 'name': 'Ilość różnych osób',
#                 'value': 2,
#             },
#             self.data['statistics'][0])

#     def test_add_top_games(self):
#         self.controller.add_top_games()

#         self.assertEqual(
#             [(2, 'first'), (1, 'second')], self.data['games'])

#     def test_add_top_people(self):
#         self.controller.add_top_people()

#         self.assertEqual(
#             [
#                 ('Franek', 'Kimono', 2),
#                 ('Ten', 'Drugi', 1),
#             ],
#             self.data['peoples'])

#     def test_make(self):
#         self.add_mock_object(self.controller, 'verify_convent')
#         self.add_mock_object(self.controller, 'get_convent')
#         self.mocks['verify_convent'].return_value = True
#         self.mocks['get_convent'].return_value = fixtures['Convent']['first']
#         self.controller.make()

#     def test_make_verify(self):
#         """StatisticsController should verify_convent and do nothing if it
#         fails"""
#         self.add_mock_object(self.controller, 'verify_convent')
#         self.add_mock_object(self.controller, 'get_convent')
#         self.mocks['verify_convent'].return_value = False

#         self.controller.make()

#         self.assertEqual(0, self.mocks['get_convent'].call_count)
