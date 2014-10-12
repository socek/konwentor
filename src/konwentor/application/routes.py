def make_routes(app, route):
    route.prefix = 'konwentor.'
    app.config.add_static_view(
        name='static',
        path=app.settings['paths:static'])
    route.read_yaml(app.settings['paths:routes'])
