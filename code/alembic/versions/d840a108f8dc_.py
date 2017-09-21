"""empty message

Revision ID: d840a108f8dc
Revises: 7157c709d8c1
Create Date: 2016-11-16 22:19:19.683933

"""
from alembic import op
from sqlalchemy import Column
from sqlalchemy import String


# revision identifiers, used by Alembic.
revision = 'd840a108f8dc'
down_revision = '7157c709d8c1'


def upgrade():
    op.add_column(
        'game_borrows',
        Column(
            'document',
            String,
            nullable=True))


def downgrade():
    pass
