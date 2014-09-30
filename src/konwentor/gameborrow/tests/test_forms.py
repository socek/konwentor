from haplugin.toster import FormTestCase, SqlFormTestCase
from haplugin.toster.fixtures import fixtures

from ..forms import GameBorrowAddForm


class GameBorrowAddFormTest(FormTestCase):
    prefix_from = GameBorrowAddForm

    def setUp(self):
        super().setUp()
        self.add_mock_object(self.form, 'get_entity')
        self.entity = self.mocks['get_entity'].return_value

    def test_get_avalible_documents(self):
        elements = self.form.get_avalible_documents()
        self.assertEqual({
            'label': '(Wybierz)',
            'value': '',
        }, elements[0])

    def test_overal_validation(self):
        """overalValidation should return GameEntity.is_avalible"""
        self.entity.is_avalible.return_value = True

        self.assertEqual(
            True,
            self.form.overalValidation({'game_entity_id': ['1']}))

        self.mocks['get_entity'].assert_called_once_with('1')

    def test_overal_validation_false(self):
        """overalValidation should return GameEntity.is_avalible"""
        self.entity.is_avalible.return_value = False

        self.assertEqual(
            False,
            self.form.overalValidation({'game_entity_id': ['1']}))

        self.mocks['get_entity'].assert_called_once_with('1')
        self.assertEqual(
            'Ta gra nie ma już wolnych kopii.',
            self.form.message)

    def test_submit(self):
        self.add_mock('GameBorrow')

        self.form.submit({
            'game_entity_id': [12],
            'name': ['sds'],
            'surname': ['zxc'],
            'document_type': ['ccs'],
            'document_number': ['wer'],
        })

        element = self.mocks['GameBorrow'].return_value

        self.assertEqual(12, element.game_entity_id)
        self.assertEqual('sds', element.name)
        self.assertEqual('zxc', element.surname)
        self.assertEqual('ccs', element.document_type)
        self.assertEqual('wer', element.document_number)
        self.assertEqual(True, element.is_borrowed)

        self.db.add.assert_called_once_with(element)
        self.db.commit.assert_called_once_with()


class SqlGameBorrowAddFormTest(SqlFormTestCase):
    prefix_from = GameBorrowAddForm

    def test_get_entity(self):
        _id = fixtures['GameEntity'][0].id
        entity = self.form.get_entity(_id)

        self.assertEqual(
            fixtures['GameEntity'][0],
            entity)
