"""Create Convent model

Revision ID: 179cfa580c7
Revises: None
Create Date: 2014-08-25 19:06:03.489845

"""

# revision identifiers, used by Alembic.
revision = '179cfa580c7'
down_revision = None

from alembic import op
from sqlalchemy import Column, Integer, String


def upgrade():
    op.create_table(
        'convents',
        Column('id', Integer, primary_key=True),
        Column('name', String()),
    )


def downgrade():
    op.drop_table('convents')
