from hatak.tests.cases import FormTestCase

from konwentor.application.forms import PostForm


class PostFormTest(FormTestCase):

    prefix_from = PostForm

    def test_call(self):
        """PostForm should use .POST data from request."""
        self.request.POST.dict_of_lists.return_value = {}
        self.form()

        self.request.POST.dict_of_lists.assert_called_once_with()
