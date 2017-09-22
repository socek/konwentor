from yaml import load


class Route(object):
    controller_values = [
        'template',
        'permission',
        'attr',
        'renderer',
        'http_cache',
        'wrapper',
        'decorator',
        'mapper',
        'context',
        'request_type',
        'request_method',
        'request_param',
        'match_param',
        'containment',
        'xhr',
        'accept',
        'header',
        'path_info',
        'check_csrf',
        'physical_path',
        'effective_principals',
        'custom_predicates',
        'predicates',
    ]

    def __init__(self, app):
        self.app = app
        self.prefix = None
        self.app.config.registry['route'] = self
        self.routes = {}

    @property
    def config(self):
        return self.app.config

    def add(self, controller, route, url, *args, **kwargs):
        self.config.add_route(
            route,
            url,
            *args,
            **kwargs)

        self.add_view(controller, route_name=route)

    def add_view(self, controller, route=None, **kwargs):
        url = self.convert_url(controller)

        controller_class = self.config.maybe_dotted(url)

        if 'route_name' in kwargs:
            self.routes[kwargs['route_name']] = controller_class

        for name in self.controller_values:
            self.set_controller_config(kwargs, controller_class, name)

        self.config.add_view(url, **kwargs)

    def convert_url(self, url):
        return self.prefix + url

    def set_controller_config(self, kwargs, controller, name):
        value = getattr(controller, name, None)
        if name == 'template' and value is not None:
            name, value = self._convert_template(name, value, controller)
        if value:
            kwargs[name] = value

    def _convert_template(self, name, value, controller):
        templates_dir = getattr(controller, 'templates_dir', 'templates')
        app, path = value.split(':')
        value = "%s%s:%s/%s" % (
            self.prefix,
            app,
            templates_dir,
            path)
        print('renderer:', value)
        return 'renderer', value

    def read_yaml(self, path):
        with open(path, 'r') as stream:
            data = load(stream)
        for name, value in self._inner_dict(data):
            value['controller'] = '%s.%s' % (
                name,
                value['controller'],)
            self.add(**value)

    def _inner_dict(self, data, prefix=''):
        for name, value in data.items():
            if type(value) is dict:
                yield from self._inner_dict(value, prefix + name + '.')
            else:
                for element in value:
                    yield (prefix + name, element)
