from sqlalchemy import func, desc, distinct, and_

from konwentor.game.models import Game
from konwentor.gameborrow.models import GameBorrow
from konwentor.gamecopy.controllers import GameCopyControllerBase
from konwentor.gamecopy.models import GameEntity, GameCopy


class StatisticsController(GameCopyControllerBase):

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
        return (
            self.db.query(GameBorrow)
            .join(GameEntity)
            .filter(GameEntity.convent == self.data['convent'])
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
            .join(GameEntity)
            .filter(GameEntity.convent == self.data['convent'])
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
            .filter(GameEntity.convent == self.data['convent'])
            .all())

    def add_top_people(self):
        self.data['peoples'] = (
            self.query(
                func.max(GameBorrow.name).label('name'),
                func.min(GameBorrow.surname).label('surname'),
                GameBorrow.document_type,
                GameBorrow.document_number,
                func.count(GameBorrow.id).label('borrows'),)
            .join(GameEntity)
            .group_by(GameBorrow.document_type, GameBorrow.document_number)
            .order_by(desc('borrows'))
            .filter(GameEntity.convent == self.data['convent'])
            .all()
        )

    def add_all_games(self):
        games = (
            self.query(func.count(distinct(Game.id)))
            .join(GameCopy)
            .join(GameEntity)
            .filter(
                and_(
                    GameEntity.convent == self.data['convent'],
                    Game.is_active.is_(True),
                ))
            .scalar())
        self.data['statistics'].append({
            'name': 'Różnych gier',
            'value': games,
        })

    def add_all_copies(self):
        copies = (
            self.query(func.sum(GameEntity.count))
            .filter(GameEntity.convent == self.data['convent'])
            .scalar())
        self.data['statistics'].append({
            'name': 'Sztuk gier',
            'value': copies,
        })
