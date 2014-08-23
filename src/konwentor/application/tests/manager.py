from toster import TestManager


def create_manager():
    manager = TestManager()
    prefix = 'konwentor.'

    cases = [
        'convent.tests.test_forms:ConventAddFormTest',
        'convent.tests.test_forms:ConventDeleteFormTest',
        'convent.tests.test_database:ConventDatabaseTest',
        'statistics.tests.test_controller:StatisticsControllerTest',
        'statistics.tests.test_controller:StatisticsSqlsTest',
    ]

    for case in cases:
        manager.add_testcase(prefix + case)

    return manager
