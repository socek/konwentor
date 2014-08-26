from mock import MagicMock

from hatak.tests.cases import FormTestCase

from ..forms import GameCopyAddForm


class GameCopyAddFormTest(FormTestCase):

    prefix_from = GameCopyAddForm

    def test_get_objects(self):
        """get_objects should return list of dicts"""
        example_model = MagicMock()
        self.query.return_value.all.return_value = [example_model]

        data = self.form.get_objects(self)

        self.assertEqual({
            'label': '(Wybierz)',
            'value': '',
        }, data[0])

        self.assertEqual({
            'label': example_model.name,
            'value': str(example_model.id),
        }, data[1])

        self.query.assert_called_with(self)
        self.query.return_value.all.assert_called_with()

    def test_submit(self):
        self.add_mock('Game')
        self.add_mock('User')
        self.add_mock('User')
        self.add_mock('Convent')
        self.add_mock_object(self.form, 'create_gamecopy', autospec=True)
        self.add_mock_object(self.form, 'create_gameentity', autospec=True)
        self.mocks['create_gameentity'].return_value.count = 3

        self.form.submit({
            'game_id': ['game_id'],
            'user_id': ['user_id'],
            'convent_id': ['convent_id'],
            'count': ['2'],
        })

        self.mocks['Game'].get_by_id.assert_called_once_with(
            self.db, 'game_id')
        self.mocks['User'].get_by_id.assert_called_once_with(
            self.db, 'user_id')
        self.mocks['Convent'].get_by_id.assert_called_once_with(
            self.db, 'convent_id')

        self.mocks['create_gamecopy'].assert_called_once_with(
            self.mocks['Game'].get_by_id.return_value,
            self.mocks['User'].get_by_id.return_value,
        )

        self.mocks['create_gameentity'].assert_called_once_with(
            self.mocks['Convent'].get_by_id.return_value,
            self.mocks['create_gamecopy'].return_value,
        )
        gameentity = self.mocks['create_gameentity'].return_value

        self.assertEqual(gameentity.count, 5)

        self.db.add.assert_called_once_with(gameentity)
        self.db.commit.assert_called_once_with()
        self.db.rollback.assert_called_once_with()
