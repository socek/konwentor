from hatak.plugin import Plugin, RequestPlugin
from hatak.controller import ControllerPlugin

from haplugin.jinja2 import Jinja2Plugin
from haplugin.beaker import BeakerPlugin

from .helpers import FlashMessageWidget
from .models import FlashMessage


class FlashMessagePlugin(Plugin):

    def add_controller_plugins(self,):
        self.add_controller_plugin(FlashMessageControllerPlugin)

    def add_unpackers(self):
        self.unpacker.add('add_flashmsg', lambda req: req.add_flashmsg)

    def add_request_plugins(self):
        self.add_request_plugin(AddFlashmsgRequestPlugin)

    def validate_plugin(self):
        self.app._validate_dependency_plugin(Jinja2Plugin)
        self.app._validate_dependency_plugin(BeakerPlugin)


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
