from hatak.application import Application
from hatak.plugins.plugin import Plugin

from konwentor.auth.plugin import AuthPlugin
from konwentor.menu.plugin import MenuPlugin
from konwentor.flashmsg.plugin import FlashMessagePlugin
from konwentor.forms.plugin import FormPlugin

from .routes import make_routes


class HamlPlugin(Plugin):

    def before_config(self):
        extensions = self.settings.get('jinja2.extensions', [])
        extensions.append('hamlish_jinja.HamlishExtension')
        self.settings['jinja2.extensions'] = extensions

    def add_to_registry(self):
        self.config.add_jinja2_renderer('.haml')


main = Application('konwentor', make_routes)
main.add_plugin(AuthPlugin())
main.add_plugin(MenuPlugin())
main.add_plugin(FlashMessagePlugin())
main.add_plugin(FormPlugin())
main.add_plugin(HamlPlugin())
