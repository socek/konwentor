from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import DateTime, Boolean

meta = MetaData()

game_entities = Table(
    'game_entities', meta,
    Column('id', Integer, primary_key=True),)

game_borrows = Table(
    'game_borrows', meta,
    Column(
        'id',
        Integer,
        primary_key=True),

    Column(
        'game_entity_id',
        Integer,
        ForeignKey('game_entities.id'),
        nullable=False),
    Column(
        'borrowed_timestamp',
        DateTime,
        default=datetime.now,
        nullable=False),
    Column(
        'return_timestamp',
        DateTime),
    Column(
        'is_borrowed',
        Boolean),

    Column(
        'name',
        String),
    Column(
        'surname',
        String),
    Column(
        'document_type',
        String),
    Column(
        'document_number',
        String),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    game_borrows.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    game_borrows.drop()
