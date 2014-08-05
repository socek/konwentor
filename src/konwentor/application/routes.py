from hatak.route import Route
from pyramid.exceptions import Forbidden


def make_routes(app):
    app.config.add_static_view(name='static', path=app.settings['static'])
    route = Route(app, 'konwentor.')

    route.add('convent.controller.ConventListController', 'convent:list', '/')
    route.add('convent.controller.ConventAdd', 'convent:add', '/convent/add')
    route.add(
        'convent.controller.ConventDelete',
        'convent:delete',
        '/convent/delete/{obj_id:\d+}')

    route.add('game.controller.GameListController', 'game:list', '/games')
    route.add('game.controller.GameAddController', 'game:add', '/game/add')
    route.add(
        'game.controller.GameDelete',
        'game:delete',
        '/game/delete/{obj_id:\d+}')

    route.add(
        'gamecopy.controller.GameCopyAddController',
        'gamecopy:add', '/gamecopy/add')

    route.add('auth.controller.LoginController', 'auth:login', '/login')
    route.add('auth.controller.LogoutController', 'auth:logout', '/logout')
    route.add_view('auth.controller.ForbiddenController', context=Forbidden)
