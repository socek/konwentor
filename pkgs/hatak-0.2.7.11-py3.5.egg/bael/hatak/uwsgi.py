from baelfire.task import Task
from baelfire.dependencies import AlwaysRebuild, PidFileIsRunning
from baelfire.dependencies import PidFileIsNotRunning


class UwsgiBase(Task):

    def uwsgi(self, command, *args, **kwargs):
        command = self.paths['exe:uwsgi'] + ' ' + command
        return self.command([command], *args, **kwargs)


class UwsgiStart(UwsgiBase):
    path = '/uwsgi/start'

    def generate_links(self):
        self.add_link('bael.hatak.tasks:Develop')

    def generate_dependencies(self):
        self.add_link('bael.hatak.tasks:Develop')
        self.add_dependecy(PidFileIsNotRunning(self.paths['uwsgi:pid']))

    def make(self):
        self.uwsgi('--ini-paste %(data:frontend.ini)s' % (self.paths))


class UwsgiStop(UwsgiBase):
    path = '/uwsgi/stop'

    def generate_dependencies(self):
        self.add_dependecy(PidFileIsRunning(self.paths['uwsgi:pid']))

    def make(self):
        with open(self.paths['uwsgi:pid'], 'r') as pidfile:
            pid = pidfile.read()
        self.command('kill -INT %s' % (pid,))


class UwsgiRestart(UwsgiStart):
    path = '/uwsgi/restart'

    def generate_dependencies(self):
        self.add_dependecy(AlwaysRebuild())

    def generate_links(self):
        super().generate_links()
        self.add_link(UwsgiStop)
