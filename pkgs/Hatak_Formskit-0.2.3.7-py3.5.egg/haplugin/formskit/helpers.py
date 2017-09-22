from haplugin.jinja2 import Jinja2HelperMany


class FormWidget(Jinja2HelperMany):

    prefix = 'haplugin.formskit:templates'

    def __init__(self, request, form):
        super().__init__(request)
        self.form = form

    def get_id(self, name):
        return '%s_%s' % (self.form.get_name(), name)

    def begin(self, id_=None, style=None):
        data = {}
        data['action'] = getattr(self.form, 'action', None)
        data['id'] = id_
        data['name'] = self.form.get_name()
        data['style'] = style
        return self.render_for('begin.jinja2', data)

    def end(self):
        return self.render_for('end.jinja2', {})

    def text(self, name, disabled=False, autofocus=False):
        return self._input('text', name, disabled, autofocus)

    def password(self, name, disabled=False, autofocus=False):
        return self._input('password', name, disabled, autofocus)

    def select(self, name, disabled=False, autofocus=False):
        return self._input('select', name, disabled, autofocus)

    def _base_input(self, name):
        data = {}
        data['name'] = self.form.fields[name].get_name()
        data['value'] = self.form.get_value(name, default='')
        data['values'] = self.form.get_values(name)
        data['field'] = self.form.fields[name]
        return data

    def _input(
        self,
        input_type,
        name,
        disabled=False,
        autofocus=False,
        prefix=None,
        **kwargs
    ):
        data = self._base_input(name)
        field = data['field']

        data['id'] = self.get_id(name)
        data['label'] = field.label
        data['error'] = field.error
        data['messages'] = field.get_error_messages()
        data['value_messages'] = field.get_value_errors(default=[])
        data['disabled'] = disabled
        data['autofocus'] = autofocus
        data.update(kwargs)
        return self.render_for(input_type + '.jinja2', data, prefix=prefix)

    def hidden(self, name):
        data = self._base_input(name)
        return self.render_for('hidden.jinja2', data)

    def csrf_token(self):
        return self.hidden('csrf_token')

    def submit(self, label='', cls='btn-success', base_cls='btn btn-lg'):
        return self.render_for(
            'submit.jinja2', {
                'label': label,
                'class': cls,
                'base_class': base_cls})

    def error(self):
        data = {}
        data['error'] = True if self.form.success is False else False
        data['messages'] = self.form.get_error_messages()
        return self.render_for('error.jinja2', data)
