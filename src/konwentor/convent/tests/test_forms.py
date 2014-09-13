from hatak.tests.cases import FormTestCase

from konwentor.convent.forms import ConventAddForm, ConventDeleteForm


class ConventAddFormTest(FormTestCase):

    prefix_from = ConventAddForm

    def test_submit(self):
        self.add_mock('Convent')
        self.form.submit({
            'name': ['myname'],
        })

        self.mocks['Convent'].create.assert_called_once_with(
            self.db, name='myname')


class ConventDeleteFormTest(FormTestCase):

    prefix_from = ConventDeleteForm

    def test_submit(self):
        self.add_mock('Convent')
        self.form.submit({
            'obj_id': ['123'],
        })

        self.mocks['Convent'].get_by_id.assert_called_once_with(
            self.db, 123)
        convent = self.mocks['Convent'].get_by_id.return_value
        self.assertEqual(False, convent.is_active)
        self.db.commit.assert_called_once_with()
