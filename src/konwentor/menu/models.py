class MenuObject(object):

    def __init__(self, widget, name, route, icon=None):
        self.widget = widget
        self.request = widget.request
        self.highlighted = widget.highlighted
        self.name = name
        self.route = route
        self.icon = icon

    def get_url(self):
        return self.request.route_path(self.route)

    def is_highlited(self):
        return self.highlighted == self.route

    def get_icon(self):
        return 'fa-' + self.icon if self.icon else ''
