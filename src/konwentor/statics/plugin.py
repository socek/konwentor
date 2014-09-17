from hatak.plugins.plugin import Plugin
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

    def add_js(self, request):
        def _append_js_code(code):
            request.registry['js_codes'].append(code)
        return _append_js_code

    def add_js_link(self, request):
        def _append_js_link(url):
            link = request.get_static(url)
            if link not in self.registry['js_links']:
                request.registry['js_links'].append(link)
        return _append_js_link

    def add_css_link(self, request):
        def _append_css_link(url):
            link = request.get_static(url)
            if link not in self.registry['css_links']:
                request.registry['css_links'].append(link)
        return _append_css_link

    def get_static(self, request):
        def _get_static(url):
            return request.static_path(self.settings['static'] + url)
        return _get_static

    def add_controller_plugins(self, plugins):
        plugins.append(StaticControllerPlugin)


class StaticControllerPlugin(ControllerPlugin):

    def make_helpers(self):
        self.add_helper(
            'static', StaticHelper)

        static = self.controller.data['static']

        static.add_css_link('/css/bootstrap.min.css')
        static.add_css_link('/css/plugins/metisMenu/metisMenu.min.css')
        static.add_css_link('/css/plugins/timeline.css')
        static.add_css_link('/css/sb-admin-2.css')
        static.add_css_link('/css/plugins/morris.css')
        static.add_css_link('/font-awesome-4.1.0/css/font-awesome.min.css')
        static.add_css_link('/css/jquery-ui.min.css')
        static.add_css_link('/css/jquery-ui.structure.min.css')
        static.add_css_link('/css/jquery-ui.theme.min.css')

        static.add_js_link('/js/jquery-1.11.0.js')
        static.add_js_link('/js/bootstrap.min.js')
        static.add_js_link('/js/plugins/metisMenu/metisMenu.min.js')
        static.add_js_link('/js/jquery-ui.min.js')
        static.add_js_link('/js/sb-admin-2.js')
