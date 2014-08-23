def make_settings(settings, paths):
    settings['db:db'] = 'konwentor_test'
    settings['db:testurl'] = (
        '%(db:type)s://%(db:login)s:%(db:password)s@%(db:host)s:%(db:port)s/'
        'postgres')
