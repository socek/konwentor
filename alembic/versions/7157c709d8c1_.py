"""empty message

Revision ID: 7157c709d8c1
Revises: 117f70b9792
Create Date: 2016-11-14 22:25:50.098163

"""

# revision identifiers, used by Alembic.
revision = '7157c709d8c1'
down_revision = '117f70b9792'

from alembic import op
from sqlalchemy import Column, String


def upgrade():
    op.add_column(
        'game_borrows',
        Column(
            'borrow_name',
            String,
            nullable=False,
            server_default='x'))
    connection = op.get_bind()
    sql = "UPDATE game_borrows SET borrow_name = name || ' ' || surname;"
    connection.execute(sql)
    op.drop_column('game_borrows', 'name')
    op.drop_column('game_borrows', 'surname')
    op.drop_column('game_borrows', 'stats_hash')


def downgrade():
    pass
