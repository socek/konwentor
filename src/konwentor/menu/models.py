from jinja2 import Markup


class MenuObject(object):

    def __init__(self, widget, name, route, icon=None, *args, **kwargs):
        self.widget = widget
        self.request = widget.request
        self.session = self.request.session
        self.highlighted = widget.highlighted
        self.name = name
        self.route = route
        self.route_args = args, kwargs
        self.icon = icon
        self.childs = []

    def get_url(self):
        if self.is_avalible() and self.route:
            return self.request.route_path(
                self.route,
                *self.route_args[0],
                **self.route_args[1]
            )
        else:
            return '#'

    def is_highlited(self):
        return self.highlighted == self.route

    def get_icon(self):
        return 'fa-' + self.icon if self.icon else ''

    def is_visible(self):
        if self.route:
            return self.request.user.has_access_to_route(self.route)
        else:
            return True

    def is_avalible(self):
        return True

    def add_child(self, *args, **kwargs):
        self.add_child_object(MenuObject(self.widget, *args, **kwargs))

    def add_child_object(self, obj):
        self.childs.append(obj)

    def get_css_class(self):
        if not self.is_avalible():
            return Markup('class="disabled"')
        elif self.is_highlited():
            return Markup('class="active"')
        else:
            return ''
