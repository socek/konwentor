from pyramid.config import Configurator
from morfdict import Factory
from importlib import import_module

import hatak
from .unpackrequest import UnpackRequest
from .command import CommandsApplication
from .errors import PluginNotFound
from .route import Route


class Application(object):

    """Prepering and configuring project."""

    route_class = Route

    def __init__(self, module, make_routes):
        self.make_routes = make_routes
        self.module = module
        self.initialize_unpacker()
        self.plugins = []
        self.plugin_types = []
        self.controller_plugins = []
        self.commands = None

    def initialize_unpacker(self):
        self.unpacker = UnpackRequest()
        self.unpacker.add('POST', lambda req: req.POST)
        self.unpacker.add('GET', lambda req: req.GET)
        self.unpacker.add('matchdict', lambda req: req.matchdict)
        self.unpacker.add('settings', lambda req: req.registry['settings'])
        self.unpacker.add('paths', lambda req: req.registry['paths'])
        self.unpacker.add('registry', lambda req: req.registry)
        self.unpacker.add('route', lambda req: req.route_path)

    def add_plugin(self, plugin):
        if type(plugin) in self.plugin_types:
            # add plugin only once
            # TODO: this should raise an error
            return
        plugin.init(self)
        plugin.add_unpackers()
        plugin.add_controller_plugins()
        self.plugin_types.append(type(plugin))
        self.plugins.append(plugin)

    def __call__(self, settings={}):
        self.generate_settings(settings)
        self.append_plugin_settings()
        self.walk_thru_plugins()
        self.make_before_config()
        self.create_config()
        self.make_after_config()
        self.make_pyramid_includes()
        self.init_routes()
        self.make_registry(self.config.registry)

        return self.config.make_wsgi_app()

    def init_routes(self):
        self.route = Route(self)
        self.make_routes(self, self.route)
        for plugin in self.plugins:
            plugin.append_routes()

    def run_commands(self, settings={}):
        self.generate_settings(settings)
        self.append_plugin_settings()
        self.commands = CommandsApplication(self)
        self.commands()

    def generate_settings(self, settings):
        self.settings, self.paths = self.get_settings(self.module, settings)
        self.settings['paths'] = self.paths
        return self.settings

    def get_settings(self, module, settings={}, additional_modules=None):
        additional_modules = additional_modules or [
            ('local', False),
        ]
        self.factory = Factory('%s.application' % (module))
        settings, paths = self.factory.make_settings(
            settings=settings,
            additional_modules=additional_modules,)
        settings['paths'] = paths
        return settings, paths

    def create_config(self):
        self.config = Configurator(
            settings=self.settings.to_dict(),
        )

    def append_plugin_settings(self):
        for plugin in self.plugins:
            plugin.append_settings()

    def walk_thru_plugins(self):
        for plugin in self.plugins:
            plugin.walk_thru_plugins()

    def make_before_config(self):
        for plugin in self.plugins:
            plugin.before_config()

    def make_after_config(self):
        for plugin in self.plugins:
            plugin.add_request_plugins()
        for plugin in self.plugins:
            plugin.after_config()

    def make_pyramid_includes(self):
        for plugin in self.plugins:
            plugin.make_config_include_if_able()
        self.config.commit()

    def make_registry(self, registry):
        registry['unpacker'] = self.unpacker
        registry['settings'] = self.settings
        registry['paths'] = self.paths
        registry['controller_plugins'] = self.controller_plugins
        for plugin in self.plugins:
            plugin.add_to_registry()

    def add_controller_plugin(self, plugin):
        self.controller_plugins.append(plugin)

    def _validate_dependency_plugin(self, plugin):
        if not plugin in self.plugin_types:
            raise PluginNotFound(plugin)

    def start_pytest_session(self):
        self.generate_settings({})
        self.append_plugin_settings()
        self.factory.run_module_without_errors('tests')
        hatak._test_cache['app'] = self

    def _import_from_string(self, url):
        url = url.split(':')
        module = import_module(url[0])
        return getattr(module, url[1])

    def get_plugin(self, cls):
        for plugin in self.plugins:
            if cls == type(plugin):
                return plugin
