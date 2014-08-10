from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import UniqueConstraint

meta = MetaData()

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

    conn.execute(permission.insert().values(group='base', name='view'))
    conn.execute(permission.insert().values(group='convent', name='add'))
    conn.execute(permission.insert().values(group='convent', name='delete'))
    conn.execute(permission.insert().values(group='game', name='add'))
    conn.execute(permission.insert().values(group='game', name='delete'))
    conn.execute(permission.insert().values(group='gamecopy', name='add'))
    conn.execute(permission.insert().values(group='gameborrow', name='add'))

    inc = (
        user.insert()
        .values(
            name='Socek',
            email='msocek@gmail.com',
            password='bc4e508c5713726a6ea9b057c10e9ddb7594ad5dd5f117873dd69eb'
            'de44d46111cc72e9796624b17')
    )
    conn.execute(inc)


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pass
