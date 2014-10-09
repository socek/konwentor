def make_settings(settings, paths):
    if settings['db:type'] == 'sqlite':
        paths['sqlite_testdb'] = ["%(data)s", 'database_test.db']
        settings['db:db'] = '%(sqlite_testdb)s' % paths
    else:
        settings['db:db'] = 'konwentor_test'
        settings['db:testurl'] = (
            '%(db:type)s://%(db:login)s:%(db:password)s@%(db:host)s:'
            '%(db:port)s/postgres')
