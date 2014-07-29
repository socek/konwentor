from hatak.controller import DatabaseController

from .models import Convent


class ConventHome(DatabaseController):

    renderer = 'convent/home.jinja2'

    def make(self):
        self.data['convents'] = self.get_convents()

    def get_convents(self):
        return self.db.query(Convent).all()
