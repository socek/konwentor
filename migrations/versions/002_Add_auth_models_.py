from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import UniqueConstraint

meta = MetaData()

users_2_permissions = Table(
    'users_2_permissions', meta,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)

user = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String()),
    Column('email', String, unique=True),
    Column('password', String(128))
)

permission = Table(
    'permissions', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String()),
    Column('group', String()),
    UniqueConstraint('name', 'group')
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    user.create()
    permission.create()
    users_2_permissions.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    users_2_permissions.drop()
    permission.drop()
    user.drop()
