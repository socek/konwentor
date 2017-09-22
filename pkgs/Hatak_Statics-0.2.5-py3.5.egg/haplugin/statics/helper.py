from haplugin.jinja2 import Jinja2HelperMany


class StaticHelper(Jinja2HelperMany):
    prefix = 'haplugin.statics:templates'

    def __init__(self, request):
        super().__init__(request)

    @property
    def js_links(self):
        return self.request.registry['js_links']

    @property
    def css_links(self):
        return self.request.registry['css_links']

    @property
    def js_codes(self):
        return self.request.registry['js_codes']

    def add_js_link(self, link, index=None):
        self.request.add_js_link(link, index)
        return ''

    def add_css_link(self, link):
        self.request.add_css_link(link)
        return ''

    def generate_js_links(self):
        return self.render_for('js_links.jinja2', {'links': self.js_links})

    def generate_css_links(self):
        return self.render_for('css_links.jinja2', {'links': self.css_links})

    def generate_js_codes(self):
        return self.render_for('js_codes.jinja2', {'codes': self.js_codes})
