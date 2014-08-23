from toster import TestRunner

from .manager import create_manager
from konwentor.application.init import Application
from konwentor.application.tests.database import TestDatabase


class TestApplication(object):
    cache = {}

    @classmethod
    def get_settings(cls):
        try:
            return cls.cache['settings']
        except KeyError:
            settings, paths = Application.get_settings_for_tests('konwentor')
            merged = settings.merged(paths)
            cls.cache['settings'] = merged.to_dict()
            return cls.cache['settings']

    @classmethod
    def get_db(cls):
        try:
            return cls.cache['db']
        except KeyError:
            cls.connect_to_db()
            return cls.cache['db']

    @classmethod
    def get_db_engine(cls):
        try:
            return cls.cache['db_engine']
        except KeyError:
            cls.connect_to_db()

    @classmethod
    def connect_to_db(cls):
        print('Recreating database...')
        database = TestDatabase(TestApplication.get_settings())
        database.recreate_database()

        print('Migrations...')
        database.make_migration()
        engine, session = database.get_engine_and_session()

        print('Creating fixtures...')
        database.generate_fixtures(session)

        cls.cache['db'] = session
        cls.cache['db_engine'] = engine

    def _is_database_needed(self):
        return (
            self.runner.args.list is False
            and self.runner.args.group in (None, 'sql')
        )

    def __call__(self):
        self.runner = self.create_runner()
        self.runner.create_parser()
        if self._is_database_needed():
            self.connect_to_db()
        self.runner()

    def create_runner(self):
        manager = create_manager()
        return TestRunner(manager)


def run():
    return TestApplication()()
