from hatak.unpackrequest import unpack

from formskit import Form


class PostForm(Form):

    def __init__(self, request):
        self.request = request
        unpack(self, self.request)
        super().__init__()

    def __call__(self, initial_data={}):
        return super().__call__(
            self.request.POST.dict_of_lists(),
            initial_data=initial_data)
