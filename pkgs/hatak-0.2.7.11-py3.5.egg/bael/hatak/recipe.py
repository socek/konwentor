from bael.project.recipe import ProjectRecipe
from baelfire.application.application import Application
from baelfire.recipe import Recipe

from .tasks import (
    CreateDataDir,
    Serve,
    BaelfireInitFile,
    ProjectTemplates,
    Develop,
    Shell,
    Tests,
    Coverage,
)

from .templates import (
    InitPy,
    Routes,
    Settings,
    FrontendIni,
    TestFixtures,
    Conftest,
    Pytestini,
    TestSettings,
    RedmeFile,
    ManagePy,
    PShell,
)

from .uwsgi import (
    UwsgiStart,
    UwsgiStop,
    UwsgiRestart,
)

from .alembic import (
    AlembicData,
    AlembicMigration,
    AlembicRevision,
    AlembicInit,
)


class HatakRecipe(Recipe):

    prefix = '/hatak'

    def create_settings(self):
        self.set_path('project:src', 'cwd', 'src')
        self.set_path('project:conftest', 'project:src', 'conftest.py')
        self.set_path('project:pytestini', 'project:src', 'pytest.ini')
        self.set_path('datadir', 'cwd', 'data')
        self.set_path('data:frontend.ini', 'datadir', 'frontend.ini')
        self.set_path('data:log', 'datadir', 'all.log')
        self.set_path(
            'uwsgi:socket', None, '/tmp/%(package:name)s.uwsgi.socket')
        self.set_path('uwsgi:pid', 'datadir', 'uwsgi.pid')
        self.set_path('uwsgi:log', 'datadir', 'uwsgi.log')
        self.set_path('uwsgi:daemonize', 'datadir', 'uwsgi.daemonize.log')
        self.set_path(
            'venv:site-packages',
            'virtualenv_path',
            'lib/python3.4/site-packages/')

        self.set_path('flags:dbversioning', 'flagsdir', 'versioning.flag')
        self.set_path('flags:dbmigration', 'flagsdir', 'dbmigration.flag')

        self.set_path('migration:main', 'cwd', 'migrations')
        self.set_path('migration:manage', 'migration:main', 'manage2.py')
        self.set_path('migration:versions', 'migration:main', 'versions')

        self.set_path('exe:pserve', 'virtualenv:bin', 'pserve')
        self.set_path('exe:pshell', 'virtualenv:bin', 'pshell')
        self.set_path('exe:uwsgi', 'virtualenv:bin', 'uwsgi')
        self.set_path(
            'exe:manage', 'virtualenv:bin', '%(package:name)s_manage')
        self.set_path(
            'exe:pytest', 'virtualenv:bin', 'py.test')
        self.set_path('exe:coverage', 'virtualenv:bin', 'coverage')

        self.settings['develop'] = True

        self.set_path('project:application', 'project:home', 'application')
        self.set_path('project:initpy', 'project:application', 'init.py')
        self.set_path('project:pshell', 'project:application', 'pshell.py')
        self.set_path('project:managepy', 'project:application', 'manage.py')
        self.set_path('project:settings', 'project:application', 'settings')
        self.set_path('readmefile', 'cwd', 'README.txt')
        self.paths['application'] = {}
        app = self.paths['application']
        app.set_path('tests', 'project:application', 'tests')
        app.set_path('fixtures', 'tests', 'fixtures.py')

        self.set_path('project:routes', 'project:application', 'routes.py')
        self.set_path('project:default', 'project:settings', 'default.py')
        self.set_path('project:testsettings', 'project:settings', 'tests.py')

        self.set_path('alembic:ini', 'datadir', 'alembic.ini')
        self.set_path('alembic:main', 'cwd', 'alembic')
        self.set_path('alembic:versions', 'alembic:main', 'versions')

        self.settings['coverage omits'] = [
            'eggs/*',
            '*/venv/*',
            '*/tests/*',
            '*/migrations/*',
            '*/routes.py',
            '*/settings/*',
        ]
        self.set_path('virtualenvdir', 'cwd', 'venv_%(package:name)s')

    def final_settings(self):
        self.set_path('flagsdir', 'datadir', 'flags')

        self.settings['packages'] = [
            'hatak==0.2.7.8',
            'coverage',
            'hatak_logging',
            'hatak_jinja2',
            'hatak_haml',
            'hatak_sql',
            'hatak_alembic',
            'hatak_beaker',
            'hatak_debugtoolbar',
            'hatak_statics',
            'pytest-cov',
            'pytest',
            'coverage==3.7.1',

            'waitress',
            'uwsgi',
        ]
        self.settings['directories'].append('project:application')
        self.settings['directories'].append('project:settings')
        self.settings['directories'].append('application:tests')
        self.settings['entry_points'] = (
            '\r\t[paste.app_factory]\n'
            '\t\tmain = %(package:name)s.application.init:main\n'
            '\t[console_scripts]\n'
            '\t\t%(package:name)s_manage = '
            '%(package:name)s.application.manage:run\n'
            ''
        )

    def gather_recipes(self):
        self.add_recipe(ProjectRecipe(False))

    def gather_tasks(self):
        self.add_task(CreateDataDir)
        self.add_task(FrontendIni)
        self.add_task(Serve)
        self.add_task(BaelfireInitFile)
        self.add_task(InitPy)
        self.add_task(Routes)
        self.add_task(ProjectTemplates)
        self.add_task(Settings)
        self.add_task(Develop)
        self.add_task(Shell)
        self.add_task(UwsgiStart)
        self.add_task(UwsgiStop)
        self.add_task(UwsgiRestart)
        self.add_task(Tests)
        self.add_task(Coverage)
        self.add_task(AlembicData)
        self.add_task(AlembicMigration)
        self.add_task(AlembicRevision)
        self.add_task(AlembicInit)
        self.add_task(TestFixtures)
        self.add_task(Conftest)
        self.add_task(Pytestini)
        self.add_task(TestSettings)
        self.add_task(RedmeFile)
        self.add_task(ManagePy)
        self.add_task(PShell)

    def _filter_task(self, task):
        return task.get_path().startswith(self.prefix)


def run():
    Application(recipe=HatakRecipe())()
