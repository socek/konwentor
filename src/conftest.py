from konwentor.application.init import main

# TODO: Is there another way to register external fixtures?
from hatak.testing import ApplicatonFixture, RequestFixture, ControllerFixture
from haplugin.sql.testing import DatabaseFixture
from konwentor.application.tests.fixtures import fixtures

__all__ = [
    'ApplicatonFixture',
    'RequestFixture',
    'ControllerFixture',
    'DatabaseFixture',
    'fixtures',
]


def pytest_sessionstart():
    main.start_pytest_session()
