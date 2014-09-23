from hatak.application import Application
from hatak.plugins import DebugtoolbarPlugin, LoggingPlugin, TosterPlugin
from hatak.plugins import StaticPlugin, BeakerPlugin, HamlPlugin, AlembicPlugin
from hatak.plugins import SqlPlugin, Jinja2Plugin

from konwentor.auth.plugin import AuthPlugin
from konwentor.flashmsg.plugin import FlashMessagePlugin
from konwentor.forms.plugin import FormPlugin
from konwentor.menu.plugin import MenuPlugin

from konwentor.application.tests.fixtures import Fixtures
from .routes import make_routes


main = Application('konwentor', make_routes)
main.add_plugin(LoggingPlugin())
main.add_plugin(Jinja2Plugin())
main.add_plugin(HamlPlugin())
main.add_plugin(SqlPlugin())
main.add_plugin(AlembicPlugin())
main.add_plugin(BeakerPlugin())
main.add_plugin(DebugtoolbarPlugin())
main.add_plugin(AuthPlugin())
main.add_plugin(MenuPlugin())
main.add_plugin(FlashMessagePlugin())
main.add_plugin(FormPlugin())
main.add_plugin(StaticPlugin())
main.add_plugin(TosterPlugin(Fixtures))
