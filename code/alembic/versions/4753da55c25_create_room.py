"""create_room

Revision ID: 4753da55c25
Revises: 3a469619f9b
Create Date: 2015-05-13 19:32:18.308255

"""

# revision identifiers, used by Alembic.
revision = '4753da55c25'
down_revision = '3a469619f9b'

from alembic import op
from sqlalchemy import Column, Integer, String, ForeignKey


def upgrade():
    op.create_table(
        'rooms',
        Column('id', Integer, primary_key=True),
        Column('name', String(), nullable=False),
        Column(
            'convent_id', Integer, ForeignKey('convents.id'), nullable=False)
    )


def downgrade():
    op.drop_table('rooms')
