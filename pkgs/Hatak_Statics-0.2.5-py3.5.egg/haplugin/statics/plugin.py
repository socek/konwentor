from hatak.plugin import Plugin
from hatak.controller import ControllerPlugin
from haplugin.jinja2 import Jinja2Plugin

from .helper import StaticHelper
from .request_plugins import AddJsRequestPlugin, AddCssLinkRequestPlugin
from .request_plugins import AddJsLinkRequestPlugin, GetStaticRequestPlugin


class StaticPlugin(Plugin):

    def add_to_registry(self):
        self.registry['js_links'] = []
        self.registry['js_codes'] = []
        self.registry['css_links'] = []

    def add_request_plugins(self):
        self.add_request_plugin(AddJsRequestPlugin)
        self.add_request_plugin(AddCssLinkRequestPlugin)
        self.add_request_plugin(AddJsLinkRequestPlugin)
        self.add_request_plugin(GetStaticRequestPlugin)

    def add_controller_plugins(self):
        self.add_controller_plugin(StaticControllerPlugin)

    def add_depedency_plugins(self):
        self.app._validate_dependency_plugin(Jinja2Plugin)


class StaticControllerPlugin(ControllerPlugin):

    def make_helpers(self):
        self.add_helper(
            'static', StaticHelper)

        static = self.controller.data['static']
        for link in self.settings.get('css', []):
            static.add_css_link(link)

        for link in reversed(self.settings.get('js', [])):
            static.add_js_link(link, 0)
