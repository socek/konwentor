def make_settings(settings, paths):
    paths['data'] = 'data'

    settings['jinja2.directories'] = '{{settings["package:name"]}}:templates'
    settings['debug'] = False
    settings['authentication_debug'] = False
    settings['session.type'] = 'file'
    settings['session.key'] = 'needtochangethis'
    settings['session.secret'] = 'needtochangethistoo'
    settings['session.cookie_on_exception'] = True

    paths['session'] = {
        'data_dir': ["%(data)s", 'sessions', 'data'],
        'lock_dir': ["%(data)s", 'sessions', 'lock'],
    }
    settings['session.data_dir'] = '%(paths:session:data_dir)s'
    settings['session.lock_dir'] = '%(paths:session:lock_dir)s'

    paths['frontend'] = ['%(data)s', 'frontend.ini']
    paths['logging'] = {
        'config': '%(frontend)s'
    }
    paths.set_path('sqlite_db', 'data', '%(db:name)s.db')
    settings['db'] = {}
    settings['db']['type'] = 'sqlite'
    settings['db']['name'] = '{{settings["package:name"]}}_develop'
    # ----------------------------------------
    # This is example postgresql configuration
    # ----------------------------------------
    # settings['db']['type'] = 'postgresql'
    # settings['db']['login'] = 'develop'
    # settings['db']['password'] = 'develop'
    # settings['db']['host'] = 'localhost'
    # settings['db']['port'] = '5432'

    paths['alembic'] = {
        'versions': 'alembic',
        'ini': ['%(data)s', 'alembic.ini'],
    }
