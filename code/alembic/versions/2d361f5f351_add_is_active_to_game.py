"""add is_active to game

Revision ID: 2d361f5f351
Revises: 35f43817d8e
Create Date: 2014-09-13 17:52:50.696321

"""

# revision identifiers, used by Alembic.
revision = '2d361f5f351'
down_revision = '35f43817d8e'

from alembic import op
from sqlalchemy import Column, Boolean


def upgrade():
    op.add_column(
        'games',
        Column('is_active', Boolean, nullable=False, server_default='true')
    )


def downgrade():
    op.drop_column('games', 'is_active')
