from hatak.route import Route
from pyramid.exceptions import Forbidden


def make_routes(app):
    app.config.add_static_view(name='static', path=app.settings['static'])
    route = Route(app, 'konwentor.')
    route.read_yaml(app.settings['routes'])

    route.add_view('auth.controller.ForbiddenController', context=Forbidden)
