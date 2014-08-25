"""Add State column to Convent

Revision ID: 39c87223255
Revises: 1c6eaf90111
Create Date: 2014-08-25 20:19:04.834495

"""

# revision identifiers, used by Alembic.
revision = '39c87223255'
down_revision = '1c6eaf90111'

from alembic import op
from sqlalchemy import Column, String


def upgrade():
    op.add_column(
        'convents',
        Column('state', String(11), default='not started'),
    )


def downgrade():
    op.drop_column('convents', 'state')
