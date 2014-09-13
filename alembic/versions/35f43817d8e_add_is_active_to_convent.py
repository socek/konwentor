"""add is_active to Convent

Revision ID: 35f43817d8e
Revises: 1fab5cb0725
Create Date: 2014-09-13 17:09:09.655290

"""

# revision identifiers, used by Alembic.
revision = '35f43817d8e'
down_revision = '1fab5cb0725'

from alembic import op
from sqlalchemy import Column, Boolean


def upgrade():
    op.add_column(
        'convents',
        Column('is_active', Boolean, nullable=False, server_default='true')
    )


def downgrade():
    op.drop_column('convents', 'is_active')
