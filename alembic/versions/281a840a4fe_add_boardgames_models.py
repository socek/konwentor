"""Add BoardGames models

Revision ID: 281a840a4fe
Revises: 27c410959bb
Create Date: 2014-08-25 19:15:21.208950

"""

# revision identifiers, used by Alembic.
revision = '281a840a4fe'
down_revision = '27c410959bb'

from alembic import op
from sqlalchemy import Column, Integer, String, ForeignKey


def upgrade():
    op.create_table(
        'games',
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
    )

    op.create_table(
        'game_copies',
        Column('id', Integer, primary_key=True),
        Column('game_id', Integer, ForeignKey('games.id'), nullable=False),
        Column('owner_id', Integer, ForeignKey('users.id'), nullable=False),
    )

    op.create_table(
        'game_entities',
        Column('id', Integer, primary_key=True),
        Column(
            'gamecopy_id',
            Integer,
            ForeignKey('game_copies.id'),
            nullable=False),
        Column(
            'convent_id',
            Integer,
            ForeignKey('convents.id'),
            nullable=False),
        Column('count', Integer, nullable=False, default=0),
    )


def downgrade():
    op.drop_table('games')
    op.drop_table('game_copies')
    op.drop_table('games')
