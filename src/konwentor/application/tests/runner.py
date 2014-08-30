from hatak.tests.runner import TestRunner

from .fixtures import Fixtures
from konwentor.application.init import main


def run():
    TestRunner(main, Fixtures)()
