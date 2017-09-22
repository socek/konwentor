from {{settings["package:name"]}}.application.init import main


def pytest_sessionstart():
    main.start_pytest_session()

