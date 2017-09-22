import sys


class CommandsApplication(object):

    def __init__(self, app):
        self.app = app
        self.commands = {}
        self.namespaces = {}

        for plugin in self.app.plugins:
            plugin.add_commands(self)

    def add_command(self, command):
        command.init(self)

        namespace = self.namespaces.get(command.namespace, {})
        namespace[command.name] = command
        self.namespaces[command.namespace] = namespace
        self.commands[command.name] = command

    def __call__(self):
        if len(sys.argv) == 1:
            self.print_list()
        else:
            self.run_command()

    def print_list(self):
        print("All commands:")
        for namespace, commands in self.namespaces.items():
            print('[%s]' % (namespace,))
            for name, command in commands.items():
                print('    %s\t%s' % (name, command.help or ''))

    def run_command(self):
        name = sys.argv[1]
        self.commands[name](sys.argv[1:])


class Command(object):

    def __init__(self, namespace, name, help=None):
        self.namespace = namespace
        self.name = name
        self.help = help

    def init(self, parent):
        self.parent = parent
        self.app = parent.app
