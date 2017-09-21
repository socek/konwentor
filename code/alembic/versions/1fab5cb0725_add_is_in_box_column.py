"""Add is_in_box column.

Revision ID: 1fab5cb0725
Revises: 39c87223255
Create Date: 2014-09-11 17:16:12.321937

"""

# revision identifiers, used by Alembic.
revision = '1fab5cb0725'
down_revision = '39c87223255'

from alembic import op
from sqlalchemy import Column, Boolean


def upgrade():
    op.add_column(
        'game_entities',
        Column(
            'is_in_box',
            Boolean,
            nullable=False,
            server_default='false'))


def downgrade():
    op.drop_column('game_entities', 'is_in_box')
