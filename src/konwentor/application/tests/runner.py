from hatak.tests.runner import TestRunner

from .fixtures import Fixtures
from .cases import cases
from konwentor.application.init import main


def run():
    runner = TestRunner(main, Fixtures)
    runner.manager.add_testcases(cases)
    runner()
