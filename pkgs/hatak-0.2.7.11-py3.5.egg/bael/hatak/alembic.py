from glob import glob
from os import path

from bael.project.virtualenv import VirtualenvTask
from baelfire.dependencies import (
    AlwaysRebuild,
    FileChanged,
)


class AlembicBase(VirtualenvTask):

    def alembic(self, command, *args, **kwargs):
        command = self.paths['exe:manage'] + ' alembic ' + command
        return self.python(command, *args, **kwargs)


class AlembicData(AlembicBase):
    name = 'Creating alembic directory'
    path = '/alembic/data'

    def generate_links(self):
        self.add_link('bael.hatak.tasks:ProjectTemplates')

    def get_output_file(self):
        return self.paths['alembic:main']

    def make(self):
        self.alembic('init')


class AlembicMigration(AlembicBase):
    name = 'Apply migration'
    path = '/alembic/migration'

    def generate_dependencies(self):
        super().generate_dependencies()
        for file_ in glob(path.join(self.paths['alembic:versions'], '*.py')):
            self.add_dependecy(FileChanged(file_))

    def get_output_file(self):
        return self.paths['flags:dbmigration']

    def generate_links(self):
        self.add_link(AlembicData)

    def make(self):
        self.alembic('upgrade %s' % (self.kwargs.get('revision', 'head')))
        self.touchme()


class AlembicRevision(AlembicBase):
    name = 'Create new revision script'
    path = '/alembic/script'

    def generate_dependencies(self):
        self.add_dependecy(AlwaysRebuild())

    def generate_links(self):
        self.add_link(AlembicData)

    def make(self):
        description = self.ask_for('description', 'Migration description')
        self.alembic('revision -m "%s"' % (description))


class AlembicInit(AlembicBase):
    name = 'Initialize database'
    path = '/alembic/init'

    def generate_dependencies(self):
        self.add_dependecy(AlwaysRebuild())

    def generate_links(self):
        self.add_link(AlembicData)

    def make(self):
        command = self.paths['exe:manage'] + ' init'
        return self.python(command)
