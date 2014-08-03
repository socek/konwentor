from hatak.plugins.jinja2 import Jinja2Helper


class FormWidget(Jinja2Helper):

    prefix = 'forms'

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
        return self.render_for(input_type, data)

    def submit(self, label=''):
        return self.render_for('submit', {'label': label})

    def error(self):
        data = {}
        data['error'] = self.form.error
        data['message'] = self.form.message
        return self.render_for('error', data)

    def get_template(self, name, prefix=None):
        prefix = prefix or self.prefix
        return '%s/%s.jinja2' % (prefix, name)

    def render_for(self, name, data):
        self.generate_data()
        self.data.update(data)
        return self.render(self.get_template(name))
