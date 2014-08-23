from konwentor.application.tests.case import ControllerTestCase
from ..controller import ConventListController


class ConventDatabaseTest(ControllerTestCase):

    prefix_from = ConventListController

    def test_all(self):
        self.add_mock('Convent')
        result = self.controller.get_convents()
        self.assertEqual(
            self.mocks['Convent'].get_all.return_value,
            result)
        self.mocks['Convent'].get_all.assert_called_once_with(self.db)
