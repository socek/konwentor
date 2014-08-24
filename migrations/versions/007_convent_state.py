from sqlalchemy import Table, Column, Integer, String, MetaData

meta = MetaData()

convent = Table(
    'convents', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String()),
)

state_column = Column('state', String(11), default='not started')


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    state_column.create(convent, populate_default=True, nullable=False)


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    state_column.drop()
