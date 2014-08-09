from hatak.application import Application

from konwentor.auth.plugin import AuthPlugin
from konwentor.menu.plugin import MenuPlugin
from konwentor.flashmsg.plugin import FlashMessagePlugin
from konwentor.forms.plugin import FormPlugin

from .routes import make_routes

main = Application('konwentor', make_routes)
main.add_plugin(AuthPlugin())
main.add_plugin(MenuPlugin())
main.add_plugin(FlashMessagePlugin())
main.add_plugin(FormPlugin())
