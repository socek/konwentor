"""Admin Account

Revision ID: fc6deff112
Revises: 281a840a4fe
Create Date: 2014-08-25 19:25:55.916895

"""

# revision identifiers, used by Alembic.
revision = 'fc6deff112'
down_revision = '281a840a4fe'

from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer

users = table(
    'users',
    column('id', Integer),
    column('name', String()),
    column('email', String()),
    column('password', String(128))
)

permissions = table(
    'permissions',
    column('id', Integer),
    column('name', String()),
    column('group', String()),
)

users_2_permissions = table(
    'users_2_permissions',
    column('user_id', Integer),
    column('permission_id', Integer),
)


def upgrade():
    op.bulk_insert(
        users,
        [
            {
                'id': 1,
                'name': 'Socek',
                'email': 'msocek@gmail.com',
                'password': (
                    'bc4e508c5713726a6ea9b057c10e9ddb7594ad5d'
                    'd5f117873dd69ebde44d46111cc72e9796624b17')
            }
        ]
    )

    op.bulk_insert(
        permissions,
        [
            {'id': 1, 'group': 'base', 'name': 'view'},
            {'id': 2, 'group': 'convent', 'name': 'add'},
            {'id': 3, 'group': 'convent', 'name': 'delete'},
            {'id': 4, 'group': 'game', 'name': 'add'},
            {'id': 5, 'group': 'game', 'name': 'delete'},
            {'id': 6, 'group': 'gamecopy', 'name': 'add'},
            {'id': 7, 'group': 'gameborrow', 'name': 'add'},
        ]
    )

    op.bulk_insert(
        users_2_permissions,
        [
            {'user_id': 1, 'permission_id': 1},
            {'user_id': 1, 'permission_id': 2},
            {'user_id': 1, 'permission_id': 3},
            {'user_id': 1, 'permission_id': 4},
            {'user_id': 1, 'permission_id': 5},
            {'user_id': 1, 'permission_id': 6},
            {'user_id': 1, 'permission_id': 7},
        ]
    )


def downgrade():
    pass
