from konwentor.convent.forms import ConventAddForm, ConventDeleteForm
from konwentor.application.tests.case import FormTestCase


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

        self.mocks['Convent'].delete_by_id.assert_called_once_with(
            self.db, 123)
