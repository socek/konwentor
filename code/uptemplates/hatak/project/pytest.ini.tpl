[pytest]
addopts = --tb=native --cov-report html --cov-config pytest.ini

[run]
branch = True
omit =
    */tests/*
    {{settings["package:name"]}}/application/init.py
    {{settings["package:name"]}}/application/manage.py
    {{settings["package:name"]}}/application/routes.py
    {{settings["package:name"]}}/application/settings/*

[html]
directory = ../htmlcov

[paths]
source =
    {{settings["package:name"]}}
