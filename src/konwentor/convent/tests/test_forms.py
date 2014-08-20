from konwentor.convent.forms import ConventAddForm, ConventDeleteForm
from konwentor.application.tests.case import FormTestCase
from ..models import Convent


class ConventAddFormTest(FormTestCase):

    prefix_from = ConventAddForm

    def test_submit(self):
        self.add_mock('Convent')
        self.form.submit({
            'name': ['myname'],
        })

        self.mocks['Convent'].assert_called_once_with(name='myname')
        self.db.add.assert_called_once_with(self.mocks['Convent'].return_value)
        self.db.commit.assert_called_once_with()


class ConventDeleteFormTest(FormTestCase):

    prefix_from = ConventDeleteForm

    def test_submit(self):
        self.form.submit({
            'obj_id': ['123'],
        })

        self.db.query.assert_called_once_with(Convent)
        self.db.query.return_value.filter_by.assert_called_once_with(id=123)
        (
            self.db.query.return_value
            .filter_by.return_value
            .one.assert_called_once_with())
        convent = (
            self.db.query.return_value.filter_by.return_value.one.return_value)

        self.db.delete.assert_called_once_with(convent)
        self.db.commit.assert_called_once_with()
