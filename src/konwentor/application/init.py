from hatak.application import Application

from .routes import make_routes

main = Application('konwentor', make_routes)