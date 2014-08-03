from hatak.plugins.jinja2 import Jinja2Helper


class FormHelper(Jinja2Helper):

    prefix = 'forms'

    def __init__(self, request, form):
        super().__init__(request)
        self.form = form

    def begin(self, id_=None):
        self.generate_data()
        self.data['action'] = getattr(self.form, 'action', None)
        self.data['id'] = id_
        self.data['name'] = self.form.name
        return self.render_for('begin')

    def end(self):
        self.generate_data()
        return self.render_for('end')

    def text(self, name, disabled=False, autofocus=False):
        return self._input('text', name, disabled, autofocus)

    def password(self, name, disabled=False, autofocus=False):
        return self._input('password', name, disabled, autofocus)

    def _input(self, input_type, name, disabled=False, autofocus=False):
        self.generate_data()
        self.data['name'] = name
        self.data['id'] = '%s_%s' % (self.form.name, name)
        self.data['label'] = self.form.get_label(name)
        self.data['error'] = self.form.get_error(name)
        self.data['message'] = self.form.get_message(name)
        self.data['value'] = self.form.get_value(name) or ''
        self.data['disabled'] = disabled
        self.data['autofocus'] = autofocus
        return self.render_for(input_type)

    def submit(self, label=''):
        self.generate_data()
        self.data['label'] = label
        return self.render_for('submit')

    def error(self):
        self.generate_data()
        self.data['error'] = self.form.error
        self.data['message'] = self.form.message
        return self.render_for('error')

    def get_template(self, name, prefix=None):
        prefix = prefix or self.prefix
        return '%s/%s.jinja2' % (prefix, name)

    def render_for(self, name):
        return self.render(self.get_template(name))
