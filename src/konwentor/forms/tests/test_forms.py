from haplugin.toster import FormTestCase

from ..models import PostForm


class PostFormTest(FormTestCase):

    prefix_from = PostForm

    def test_call(self):
        """PostForm should use .POST data from request."""
        self.request.POST.dict_of_lists.return_value = {}
        self.form()

        self.request.POST.dict_of_lists.assert_called_once_with()
