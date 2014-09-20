"""add_game_descriptions

Revision ID: 16de96e7f7a
Revises: 2d361f5f351
Create Date: 2014-09-20 14:44:04.117732

"""

# revision identifiers, used by Alembic.
revision = '16de96e7f7a'
down_revision = '2d361f5f351'

from alembic import op
from sqlalchemy import Column, String

names = [
    'players_description',
    'time_description',
    'type_description',
    'difficulty',
]


def upgrade():
    for name in names:
        op.add_column('games', Column(name, String))


def downgrade():
    for name in names:
        op.drop_column('games', Column(name, String))
