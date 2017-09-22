def make_settings(settings, paths):
    paths['sqlite_db'] = ["%(data)s", 'test_database.db']
    settings['db:url'] = 'sqlite:///%(sqlite_db)s' % paths
    settings['db:testurl'] = 'sqlite:///%(sqlite_db)s' % paths
