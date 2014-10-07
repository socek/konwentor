from hatak.application import Application

from haplugin.logging import LoggingPlugin
from haplugin.jinja2 import Jinja2Plugin
from haplugin.haml import HamlPlugin
from haplugin.sql import SqlPlugin
from haplugin.alembic import AlembicPlugin
from haplugin.beaker import BeakerPlugin
from haplugin.debugtoolbar import DebugtoolbarPlugin
from haplugin.toster import TosterPlugin
from haplugin.statics import StaticPlugin
from haplugin.flashmsg import FlashMessagePlugin

from konwentor.forms.helpers import FormWidget
from haplugin.formskit import FormPlugin

from konwentor.auth.plugin import AuthPlugin
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
main.add_plugin(FormPlugin(FormWidget))
main.add_plugin(StaticPlugin())
main.add_plugin(TosterPlugin(Fixtures))
