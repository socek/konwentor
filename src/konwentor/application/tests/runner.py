from toster import TestRunner

from .manager import create_manager


def create_runner():
    manager = create_manager()
    return TestRunner(manager)


def run():
    return create_runner()()
