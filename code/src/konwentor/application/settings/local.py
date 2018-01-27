from os import environ


def make_settings(settings, paths):
    settings['debug'] = False
    settings['pyramid.reload_templates'] = False

    # ----------------------------------------
    # This is example postgresql configuration
    # ----------------------------------------
    settings['db:url'] = (
        '%(db:type)s://%(db:login)s:%(db:password)s@%(db:host)s:%(db:port)s'
        '/%(db:db)s')
    settings['db:type'] = 'postgresql'
    settings['db:login'] = environ['POSTGRES_USER']
    settings['db:password'] = environ['POSTGRES_PASSWORD']
    settings['db:host'] = 'postgres'
    settings['db:port'] = '5432'
    settings['db:name'] = environ['POSTGRES_DB']

    settings['session.key'] = environ['APP_SESSION_KEY']
    settings['session.secret'] = environ['APP_SESSION_SECRET']
