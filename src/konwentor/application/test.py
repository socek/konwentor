from soktest.runner import TestRunner

import konwentor
from konwentor.application.init import Application


def get_settings():
    settings, paths = Application.get_settings('konwentor')
    merged = settings.merged(paths)
    return merged.to_dict()


def get_runner():
    settings = get_settings()
    runner = TestRunner(konwentor, log_file_dir=settings['logging:tests'])
    return runner


def run():
    return get_runner().do_tests()


def testSuite():
    return get_runner().get_all_test_suite()
