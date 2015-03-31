from hatak.application import Application

# External plugins
from haplugin.logging import LoggingPlugin
from haplugin.jinja2 import Jinja2Plugin
from haplugin.haml import HamlPlugin
from haplugin.sql import SqlPlugin
from haplugin.alembic import AlembicPlugin
from haplugin.beaker import BeakerPlugin
from haplugin.debugtoolbar import DebugtoolbarPlugin
from haplugin.statics import StaticPlugin
from haplugin.auth import AuthPlugin
from haplugin.formskit import FormPlugin
from haplugin.flashmsg import FlashMessagePlugin

# Drivers
from .tests.fixtures import Fixtures
sql = SqlPlugin(Fixtures)

# Internal plugins
from konwentor.menu.plugin import MenuPlugin

# Configuration
from konwentor.forms.helpers import FormWidget
from .routes import make_routes

main = Application('konwentor', make_routes)
main.add_plugin(LoggingPlugin())
main.add_plugin(Jinja2Plugin())
main.add_plugin(HamlPlugin())
main.add_plugin(sql)
main.add_plugin(AlembicPlugin())
main.add_plugin(BeakerPlugin())
main.add_plugin(DebugtoolbarPlugin())
main.add_plugin(StaticPlugin())
main.add_plugin(AuthPlugin())
main.add_plugin(FormPlugin(FormWidget))
main.add_plugin(MenuPlugin())
main.add_plugin(FlashMessagePlugin())
