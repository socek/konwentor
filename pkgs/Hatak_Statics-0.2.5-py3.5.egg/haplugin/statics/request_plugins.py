from hatak.plugin import RequestPlugin


class AddJsRequestPlugin(RequestPlugin):

    def __init__(self):
        super().__init__('add_js')

    def __call__(self, code):
        if code not in self.registry['js_codes']:
            self.registry['js_codes'].append(code)
        return ''


class AddCssLinkRequestPlugin(RequestPlugin):

    def __init__(self):
        super().__init__('add_css_link')

    def __call__(self, url):
        link = self.request.get_static(url)
        if link not in self.registry['css_links']:
            self.registry['css_links'].append(link)


class AddJsLinkRequestPlugin(RequestPlugin):

    def __init__(self):
        super().__init__('add_js_link')

    def __call__(self, url, index=None):
        link = self.request.get_static(url)
        if link not in self.registry['js_links']:
            if index is None:
                self.registry['js_links'].append(link)
            else:
                self.registry['js_links'].insert(index, link)


class GetStaticRequestPlugin(RequestPlugin):

    def __init__(self):
        super().__init__('get_static')

    def __call__(self, url):
        return self.request.static_path(self.paths['static'] + url)
