"""add_room_for_every_convent

Revision ID: 6ae16d0ce9
Revises: 3a469619f9b
Create Date: 2015-05-03 16:35:29.124111

"""

# revision identifiers, used by Alembic.
revision = '6ae16d0ce9'
down_revision = '3a469619f9b'

from alembic import op


def upgrade():
    conn = op.get_bind()
    res = conn.execute("""
        select
            convents.id,
            (select count(*) from rooms where convent_id=convents.id)
        from convents
        group by
            convents.id
        ;
    """)
    results = res.fetchall()
    for data in results:
        if data[1] == 0:
            conn.execute("""
                insert into rooms(name, convent_id) values('Planszówki', %d)
            """.strip() % (data[0],))


def downgrade():
    pass
