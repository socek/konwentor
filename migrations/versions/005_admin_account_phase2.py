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
    conn = migrate_engine.connect()

    socek = conn.execute(
        user.select().where(user.c.email == 'msocek@gmail.com')).fetchone()

    statement = permission.select()
    for perm in conn.execute(statement).fetchall():
        inc = users_2_permissions.insert().values(
            user_id=socek.id,
            permission_id=perm.id)
        conn.execute(inc)


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pass
