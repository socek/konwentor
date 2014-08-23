from migrate.versioning.api import version_control, upgrade
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from konwentor.application.tests.fixtures import Fixtures


class TestDatabase(object):

    def __init__(self, settings):
        self.settings = settings

    def recreate_database(self):
        url = self.settings['db:testurl']
        engine = create_engine(url)

        connection = engine.connect()
        connection.execute("commit")
        connection.execute("drop database if exists konwentor_test")
        connection.execute("commit")
        connection.execute("create database konwentor_test")
        connection.close()

    def make_migration(self):
        url = self.settings['db:url']
        version_control(url, repository='migrations')
        upgrade(url, repository='migrations')

    def get_engine_and_session(self):
        url = self.settings['db:url']
        engine = create_engine(url)
        session = sessionmaker(bind=engine)()
        return engine, session

    def generate_fixtures(self, db):
        Fixtures(db)()
