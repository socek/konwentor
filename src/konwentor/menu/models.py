class MenuObject(object):

    def __init__(self, widget, name, route, icon=None):
        self.widget = widget
        self.request = widget.request
        self.session = self.request.session
        self.highlighted = widget.highlighted
        self.name = name
        self.route = route
        self.icon = icon
        self.childs = []

    def get_url(self):
        if self.route:
            return self.request.route_path(self.route)
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

    def add_child(self, *args, **kwargs):
        self.childs.append(MenuObject(self.widget, *args, **kwargs))
