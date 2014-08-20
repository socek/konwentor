from toster import TestManager


def create_manager():
    manager = TestManager()

    cases = [
        'konwentor.convent.tests.test_forms:ConventAddFormTest',
    ]

    for case in cases:
        manager.add_testcase(case)

    return manager
