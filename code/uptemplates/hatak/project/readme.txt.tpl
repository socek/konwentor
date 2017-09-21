This project is made by using "hatak". The best way to run this as development
server is to install hatak first:

    pip install hatak

and then run it as development server:

    hatak /serve

Other commands:

    hatak /tests
    hatak /alembic/script <- new migration revision

    Running uwsgi:
    hatak /uwsgi/start
    hatak /uwsgi/stop
    hatak /uwsgi/restart
