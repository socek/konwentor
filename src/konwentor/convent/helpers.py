from hatak.plugins.jinja2 import Jinja2HelperMany


def has_access_to_route(route):
    def decorator(method):
        def run_if_able(self, *args, **kwargs):
            if self.user.has_access_to_route(route):
                return method(self, *args, **kwargs)
            else:
                return ''
        return run_if_able
    return decorator


class ConventWidget(Jinja2HelperMany):

    prefix = 'convent/widget'

    STATES = {
        'not started': 'Nie ropoczęto',
        'running': 'W trakcie',
        'ended': 'Zakończony',
    }

    def __init__(self, request, convent):
        super().__init__(request)
        self.convent = convent

    @property
    def name(self):
        return self.convent.name

    @property
    def state(self):
        return self.STATES[self.convent.state]

    @has_access_to_route('convent:choose')
    def switch(self):
        return self.render_for('choose_button', {
            'url': self.route('convent:choose', obj_id=self.convent.id)
        })

    @has_access_to_route('convent:delete')
    def delete(self):
        return self.render_for('delete_button', {
            'url': self.route('convent:delete', obj_id=self.convent.id)
        })

    def start(self):
        if self.convent.is_user_able_to_start(self.user):
            return self.render_for('start_button', {
                'url': self.route('convent:start', obj_id=self.convent.id),
                'convent': self.convent,
            })
        else:
            return ''

    def end(self):
        if self.convent.is_user_able_to_end(self.user):
            return self.render_for('end_button', {
                'url': self.route('convent:end', obj_id=self.convent.id),
                'convent': self.convent,
            })
        else:
            return ''

    def edned_warning(self):
        if self.convent.state == 'ended':
            return self.render_for('ended_warning', {})
        else:
            return ''
