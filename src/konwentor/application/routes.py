from hatak.route import Route


def make_routes(app):
    app.config.add_static_view(name='static', path=app.settings['static'])
    route = Route(app, 'konwentor.')
    route.add('convent.controller.ConventHome', 'convent:home', '/')

    route.add('auth.controller.LoginController', 'auth:login', '/login')
