from hatak.plugin import Plugin, RequestPlugin
from hatak.controller import ControllerPlugin

from .helpers import FlashMessageWidget
from .models import FlashMessage


class FlashMessagePlugin(Plugin):

    def add_controller_plugins(self, plugins):
        plugins.append(FlashMessageControllerPlugin)

    def add_unpackers(self, unpacker):
        unpacker.add('add_flashmsg', lambda req: req.add_flashmsg)

    def add_request_plugins(self):
        self.add_request_plugin(AddFlashmsgRequestPlugin)


class AddFlashmsgRequestPlugin(RequestPlugin):

    def __init__(self):
        super().__init__('add_flashmsg')

    def __call__(self, *args, **kwargs):
        data = self.request.session.get('flash_messages', [])
        data.append(FlashMessage(*args, **kwargs).to_dict())
        self.request.session['flash_messages'] = data


class FlashMessageControllerPlugin(ControllerPlugin):

    def make_helpers(self):
        self.add_helper('flashmsg', FlashMessageWidget)
