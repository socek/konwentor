from sqlalchemy import func, desc

from konwentor.game.models import Game
from konwentor.gameborrow.models import GameBorrow
from konwentor.gamecopy.controller import GameCopyControllerBase
from konwentor.gamecopy.models import GameEntity, GameCopy


class StatisticsController(GameCopyControllerBase):

    renderer = 'statistics/all.jinja2'
    permissions = [('base', 'view'), ]
    menu_highlighted = 'statistics:all'

    def make(self):
        if not self.verify_convent():
            return

        self.data['convent'] = self.get_convent()
        self.data['borrows'] = self.get_borrows(self.data['convent'])
        self.data['statistics'] = []

        self.add_all_borrows()
        self.add_all_people()

        self.add_top_games()

    def get_borrows(self, convent):
        return (
            self.db.query(GameBorrow)
            .filter(GameEntity.convent == convent)
            .all())

    def add_all_borrows(self):
        self.data['statistics'].append({
            'name': 'Wypożyczonych gier',
            'value': len(self.data['borrows']),
        })

    def add_all_people(self):
        peoples = (
            self.query(GameBorrow.document_type, GameBorrow.document_number)
            .group_by(GameBorrow.document_type, GameBorrow.document_number)
        )
        self.data['statistics'].append({
            'name': 'Ilość różnych osób',
            'value': peoples.count(),
            })

    def add_top_games(self):
        self.data['games'] = (
            self.db
            .query(
                func.count(GameBorrow.id).label('borrows'),
                Game.name)
            .join(GameEntity)
            .join(GameCopy)
            .join(Game)
            .group_by(Game.id)
            .order_by(desc('borrows'))
            .all())
