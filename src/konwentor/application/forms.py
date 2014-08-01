from formskit import Form


class PostForm(Form):

    def __init__(self, request):
        self.request = request
        self.registry = request.registry
        self.db = self.registry['db']
        self.session = request.session
        super().__init__()

    def __call__(self, initial_data={}):
        return super(
            PostForm, self).__call__(self.request.POST.dict_of_lists(),
                                     initial_data=initial_data)

    def to_flat_dict(self):
        data = {}
        for key, value in self.data.items():
            data[key] = value[0]
        return data
