from sqlalchemy import Table, Column, Integer, String, MetaData

meta = MetaData()

convent = Table(
    'convents', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String()),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    convent.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    convent.drop()
