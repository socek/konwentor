from hatak.application import Application
from hatak.plugins.haml import HamlPlugin

from konwentor.auth.plugin import AuthPlugin
from konwentor.menu.plugin import MenuPlugin
from konwentor.flashmsg.plugin import FlashMessagePlugin
from konwentor.forms.plugin import FormPlugin
from konwentor.statics.plugin import StaticPlugin

from .routes import make_routes


main = Application('konwentor', make_routes)
main.add_plugin(AuthPlugin())
main.add_plugin(MenuPlugin())
main.add_plugin(FlashMessagePlugin())
main.add_plugin(FormPlugin())
main.add_plugin(HamlPlugin())
main.add_plugin(StaticPlugin())
