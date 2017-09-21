from haplugin.jinja2 import Jinja2HelperMany
from konwentor.convent.helpers import has_access_to_route


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


class UserWidget(Jinja2HelperMany):

    prefix = 'konwentor.auth:templates/widget'

    def __init__(self, request, user):
        super().__init__(request)
        self.model = user

    @property
    def id(self):
        return self.model.id

    @property
    def name(self):
        return self.model.name

    @property
    def email(self):
        return self.model.email

    @property
    def permissions(self):
        for permission in self.model.permissions:
            yield '%s:%s' % (permission.group, permission.name)

    def permission_widget(self):
        return self.render_for('permissions.haml', {'model': self})

    @has_access_to_route('auth:edit')
    def edit(self):
        return self.render_for('edit.haml', {
            'url': self.route('auth:edit', obj_id=self.model.id),
        })
