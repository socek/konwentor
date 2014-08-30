from hatak.plugins.jinja2 import Jinja2HelperSingle

from .models import FlashMessage


class FlashMessageWidget(Jinja2HelperSingle):

    template = 'konwentor.flashmsg:templates/main.jinja2'

    def make(self):
        self.data['messages'] = []
        for data in self.session.get('flash_messages', []):
            obj = FlashMessage()
            obj.from_dict(data)
            self.data['messages'].append(obj)
        self.session['flash_messages'] = []
