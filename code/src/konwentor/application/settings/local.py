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
    settings['db:login'] = 'konwentor'
    settings['db:password'] = 'iamsuperkonwent'
    settings['db:host'] = 'localhost'
    settings['db:port'] = '5432'
    settings['db:name'] = 'konwentor_live'

    settings['session.key'] = 'this899312beprivet'
    settings['session.secret'] = 'priva1e11322185oryeah'
