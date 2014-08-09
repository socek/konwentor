from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

meta = MetaData()

user = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String()),
    Column('email', String, unique=True),
    Column('password', String(128))
)

convent = Table(
    'convents', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String()),
)

games = Table(
    'games', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
)

game_copies = Table(
    'game_copies', meta,
    Column('id', Integer, primary_key=True),
    Column('game_id', Integer, ForeignKey('games.id'), nullable=False),
    Column('owner_id', Integer, ForeignKey('users.id'), nullable=False),
)

game_entities = Table(
    'game_entities', meta,
    Column('id', Integer, primary_key=True),
    Column('gamecopy_id', Integer,
           ForeignKey('game_copies.id'), nullable=False),
    Column('convent_id', Integer, ForeignKey('convents.id'), nullable=False),
    Column('count', Integer, nullable=False, default=0)
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    games.create()
    game_copies.create()
    game_entities.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    game_entities.drop()
    game_copies.drop()
    games.drop()
