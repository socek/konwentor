from hatak.plugins.plugin import Plugin, reify
from hatak.controller import ControllerPlugin

from .helper import StaticHelper


class StaticPlugin(Plugin):

    def add_to_registry(self):
        self.registry['js_links'] = []
        self.registry['js_codes'] = []
        self.registry['css_links'] = []

    def after_config(self):
        self.config.add_request_method(
            self.add_js, 'add_js', reify=True)
        self.config.add_request_method(
            self.add_js_link, 'add_js_link', reify=True)
        self.config.add_request_method(
            self.add_css_link, 'add_css_link', reify=True)
        self.config.add_request_method(
            self.get_static, 'get_static', reify=True)

    @reify
    def add_js(self, request, code):
        if code not in request.registry['js_codes']:
            request.registry['js_codes'].append(code)
        return ''

    @reify
    def add_js_link(self, request, url):
        link = request.get_static(url)
        if link not in self.registry['js_links']:
            request.registry['js_links'].append(link)

    @reify
    def add_css_link(self, request, url):
        link = request.get_static(url)
        if link not in self.registry['css_links']:
            request.registry['css_links'].append(link)

    @reify
    def get_static(self, request, url):
        return request.static_path(self.settings['static'] + url)

    def add_controller_plugins(self, plugins):
        plugins.append(StaticControllerPlugin)


class StaticControllerPlugin(ControllerPlugin):

    def make_helpers(self):
        self.add_helper(
            'static', StaticHelper)

        static = self.controller.data['static']
        for link in self.settings.get('css', []):
            static.add_css_link(link)

        for link in self.settings.get('js', []):
            static.add_js_link(link)
