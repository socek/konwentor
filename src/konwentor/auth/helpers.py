from haplugin.jinja2 import Jinja2HelperMany


def render_when_has_access(method):
    def wrapper(self, name, route, *args, **kwargs):
        if self.user.has_access_to_route(route):
            return method(self, name, route, *args, **kwargs)
        else:
            return ''
    return wrapper


class LinkWidget(Jinja2HelperMany):

    prefix = 'konwentor.auth:templates/'

    @render_when_has_access
    def button(self, name, route, *args, **kwargs):
        return self.render_for('button.haml', {
            'url': self.route(route, *args, **kwargs),
            'name': name,
        })

    @render_when_has_access
    def link(self, name, route, *args, **kwargs):
        return self.render_for('link.haml', {
            'url': self.route(route, *args, **kwargs),
            'name': name,
        })
