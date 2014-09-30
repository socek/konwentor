from hatak.plugin import Plugin
from hatak.controller import ControllerPlugin

from .helpers import FlashMessageWidget
from .models import FlashMessage


class FlashMessagePlugin(Plugin):

    def add_controller_plugins(self, plugins):
        plugins.append(FlashMessageControllerPlugin)

    def add_unpackers(self, unpacker):
        unpacker.add('add_flashmsg', lambda req: req.add_flashmsg)

    def after_config(self):
        self.config.add_request_method(
            self.add_flashmsg,
            'add_flashmsg',
            reify=True)

    def add_flashmsg(self, request):
        def add(*args, **kwargs):
            data = request.session.get('flash_messages', [])
            data.append(FlashMessage(*args, **kwargs).to_dict())
            request.session['flash_messages'] = data
        return add


class FlashMessageControllerPlugin(ControllerPlugin):

    def make_helpers(self):
        self.add_helper('flashmsg', FlashMessageWidget)
