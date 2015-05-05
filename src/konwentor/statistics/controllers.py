from konwentor.gamecopy.controllers import ConventController


class StatisticsController(ConventController):

    template = 'statistics:all.jinja2'
    permissions = [('base', 'view'), ]
    menu_highlighted = 'statistics:all'

    def make(self):
        if not self.verify_convent():
            return

        self.data['convent'] = self.get_convent()
        self.data['borrows'] = self.get_borrows()
        self.data['statistics'] = []

        self.add_top_games()
        self.add_top_people()

        self.add_all_borrows()
        self.add_all_people()
        self.add_all_games()
        self.add_all_copies()

    def get_borrows(self):
        return self.driver.GameBorrow.get_for_convent(self.data['convent'])

    def add_all_borrows(self):
        self.data['statistics'].append({
            'name': 'Wypożyczonych gier',
            'value': len(self.data['borrows']),
        })

    def add_all_people(self):
        peoples = self.driver.GameBorrow.get_people_for_convent(
            self.data['convent'])
        self.data['statistics'].append({
            'name': 'Ilość różnych osób',
            'value': peoples.count(),
        })

    def add_top_games(self):
        self.data['games'] = self.driver.Game.top_games_view(
            self.data['convent'])

    def add_top_people(self):
        self.data['peoples'] = self.driver.GameBorrow.peoples_view(
            self.data['convent'])

    def add_all_games(self):
        games = self.driver.Game.games_count_for_convent_view(
            self.data['convent'])
        self.data['statistics'].append({
            'name': 'Różnych gier',
            'value': games,
        })

    def add_all_copies(self):
        copies = self.driver.GameCopy.count_for_convent(self.data['convent'])
        self.data['statistics'].append({
            'name': 'Sztuk gier',
            'value': copies,
        })
