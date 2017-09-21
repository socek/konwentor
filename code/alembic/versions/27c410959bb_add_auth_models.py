"""Add auth models

Revision ID: 27c410959bb
Revises: 179cfa580c7
Create Date: 2014-08-25 19:09:38.018553

"""

# revision identifiers, used by Alembic.
revision = '27c410959bb'
down_revision = '179cfa580c7'

from alembic import op
from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey


def upgrade():
    op.create_table(
        'users',
        Column('id', Integer, primary_key=True),
        Column('name', String()),
        Column('email', String, unique=True),
        Column('password', String(128))
    )

    op.create_table(
        'permissions',
        Column('id', Integer, primary_key=True),
        Column('name', String()),
        Column('group', String()),
        UniqueConstraint('name', 'group'),
    )

    op.create_table(
        'users_2_permissions',
        Column('user_id', Integer, ForeignKey('users.id')),
        Column('permission_id', Integer, ForeignKey('permissions.id'))
    )


def downgrade():
    op.drop_table('users_2_permissions')
    op.drop_table('permissions')
    op.drop_table('users')
