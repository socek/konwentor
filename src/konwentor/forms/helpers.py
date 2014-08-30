from hatak.plugins.jinja2 import Jinja2HelperMany


class FormWidget(Jinja2HelperMany):

    prefix = 'konwentor.forms:templates'

    def __init__(self, request, form):
        super().__init__(request)
        self.form = form

    def begin(self, id_=None):
        data = {}
        data['action'] = getattr(self.form, 'action', None)
        data['id'] = id_
        data['name'] = self.form.name
        return self.render_for('begin', data)

    def end(self):
        return self.render_for('end', {})

    def text(self, name, disabled=False, autofocus=False):
        return self._input('text', name, disabled, autofocus)

    def password(self, name, disabled=False, autofocus=False):
        return self._input('password', name, disabled, autofocus)

    def select(self, name, disabled=False, autofocus=False):
        return self._input('select', name, disabled, autofocus)

    def _input(self, input_type, name, disabled=False, autofocus=False):
        data = {}
        data['name'] = name
        data['id'] = '%s_%s' % (self.form.name, name)
        data['label'] = self.form.get_label(name)
        data['error'] = self.form.get_error(name)
        data['message'] = self.form.get_message(name)
        data['value'] = self.form.get_value(name) or ''
        data['disabled'] = disabled
        data['autofocus'] = autofocus
        data['field'] = self.form.field_patterns[name]
        return self.render_for(input_type, data)

    def hidden(self, name):
        data = {}
        data['name'] = name
        data['value'] = self.form.get_value(name) or ''
        return self.render_for('hidden', data)

    def submit(self, label='', cls='btn-success'):
        return self.render_for('submit', {'label': label, 'class': cls})

    def error(self):
        data = {}
        data['error'] = self.form.error
        data['message'] = self.form.message
        return self.render_for('error', data)
