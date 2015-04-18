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
from konwentor.auth.plugin import KonwentorAuthPlugin
from haplugin.formskit import FormPlugin
from haplugin.flashmsg import FlashMessagePlugin

# Drivers
from .tests.fixtures import Fixtures
from konwentor.convent.driver import ConventDriver
from konwentor.game.driver import GameDriver
from konwentor.gameborrow.driver import GameBorrowDriver
from konwentor.gamecopy.driver import GameCopyDriver, GameEntityDriver
from konwentor.auth.driver import UserDriver, PermissionDriver
sql = SqlPlugin(Fixtures)
sql.add_group(ConventDriver())
sql.add_group(GameDriver())
sql.add_group(GameBorrowDriver())
sql.add_group(GameCopyDriver())
sql.add_group(GameEntityDriver())
sql.add_group(UserDriver())
sql.add_group(PermissionDriver())

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
main.add_plugin(KonwentorAuthPlugin())
main.add_plugin(FormPlugin(FormWidget))
main.add_plugin(MenuPlugin())
main.add_plugin(FlashMessagePlugin())
