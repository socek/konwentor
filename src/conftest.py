from konwentor.application.init import main

# TODO: Is there another way to register external fixtures?
from hatak.testing import ApplicatonFixture, RequestFixture, ControllerFixture
from haplugin.sql.testing import DatabaseFixture

__all__ = [
    'ApplicatonFixture',
    'RequestFixture',
    'ControllerFixture',
    'DatabaseFixture',
]


def pytest_sessionstart():
    main.start_pytest_session()
