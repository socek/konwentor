from hatak.application import Application

from haplugin.logging import LoggingPlugin
from haplugin.jinja2 import Jinja2Plugin
from haplugin.haml import HamlPlugin
from haplugin.sql import SqlPlugin
from haplugin.alembic import AlembicPlugin
from haplugin.beaker import BeakerPlugin
from haplugin.debugtoolbar import DebugtoolbarPlugin
from haplugin.statics import StaticPlugin
from haplugin.flashmsg import FlashMessagePlugin
from haplugin.auth import AuthPlugin

from konwentor.forms.helpers import FormWidget
from haplugin.formskit import FormPlugin

from konwentor.menu.plugin import MenuPlugin

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
