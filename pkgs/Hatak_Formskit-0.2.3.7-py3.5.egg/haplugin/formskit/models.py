from pyramid.session import check_csrf_token
from hatak.unpackrequest import unpack

from formskit import Form
from formskit.formvalidators import FormValidator
from formskit.translation import Translation


class PostForm(Form):

    def __init__(self, request):
        self.request = request
        unpack(self, self.request)
        super().__init__()

        self.add_form_validator(CsrfMustMatch())
        self.init_csrf()

    def reset(self):
        super().reset()
        self.init_csrf()

    def init_csrf(self):
        self.add_field('csrf_token')
        self.set_value('csrf_token', self.session.get_csrf_token())

    def validate(self):
        return super().validate(self.request.POST.dict_of_lists())

    @property
    def translation_class(self):
        return self.settings.get('form_message', Translation)


class CsrfMustMatch(FormValidator):

    message = "CSRF token do not match!"

    def validate(self):
        self.form.POST['csrf_token'] = self.form.get_value('csrf_token')
        return check_csrf_token(self.form.request, raises=False)
