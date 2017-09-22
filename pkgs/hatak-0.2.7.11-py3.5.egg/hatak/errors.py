class PluginNotFound(Exception):

    def __init__(self, plugin):
        self.plugin = plugin

    def __repr__(self):
        return 'PluginNotFound: ' + self.plugin.__name__
