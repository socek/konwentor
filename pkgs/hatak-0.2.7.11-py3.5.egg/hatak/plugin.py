from hatak.unpackrequest import unpack


class Plugin(object):

    @property
    def config(self):
        return self.app.config

    @property
    def registry(self):
        return self.config.registry

    @property
    def settings(self):
        return self.app.settings

    @property
    def paths(self):
        return self.app.paths

    @property
    def unpacker(self):
        return self.app.unpacker

    @property
    def controller(self):
        return self.app.controller_plugins

    @property
    def route(self):
        return self.app.route

    def init(self, app):
        self.app = app
        self.validate_plugin()

    def make_config_include_if_able(self):
        try:
            self.config.include(self.get_include_name())
        except NotImplementedError:
            pass

    def append_settings(self):
        pass

    def get_include_name(self):
        raise NotImplementedError()

    def add_to_registry(self):
        pass

    def before_config(self):
        pass

    def after_config(self):
        pass

    def add_unpackers(self):
        pass

    def add_controller_plugins(self):
        pass

    def add_controller_plugin(self, plugin):
        def append_parent_wrapper(controller):
            return plugin(self, controller)
        self.controller.append(append_parent_wrapper)

    def add_commands(self, parent):
        pass

    def validate_plugin(self):
        pass

    def add_request_plugins(self):
        pass

    def add_request_plugin(self, plugin):
        plugin = plugin()
        plugin.set_parent(self)
        self.config.add_request_method(
            plugin.init,
            plugin.name,
            reify=True)

    def append_routes(self):
        pass

    def walk_thru_plugins(self):
        if hasattr(self, 'interract_with'):
            for plugin in self.app.plugins:
                if plugin is not self:
                    self.interract_with(plugin)


class RequestPlugin(object):

    def __init__(self, name):
        self.name = name
        self._block = False

    def set_parent(self, parent):
        self.parent = parent

    def init(self, request):
        unpack(self, request)
        return self.return_once()

    def return_once(self):
        return self


def reify(method):
    """Decorator for making reify methods with request instance for request."""

    def requester(self, request):
        def on_request(*args, **kwargs):
            return method(self, request, *args, **kwargs)
        return on_request
    return requester
