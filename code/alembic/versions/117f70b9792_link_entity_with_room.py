"""link_entity_with_room

Revision ID: 117f70b9792
Revises: 6ae16d0ce9
Create Date: 2015-05-06 21:27:55.604885

"""

# revision identifiers, used by Alembic.
revision = '117f70b9792'
down_revision = '6ae16d0ce9'

from alembic import op
from sqlalchemy import Column, Integer, ForeignKey


def upgrade():
    op.add_column(
        'game_entities',
        Column('room_id', Integer, ForeignKey('rooms.id'))
    )
    conn = op.get_bind()
    res = conn.execute("""
        select
            game_entities.id,
            (select min(rooms.id) from rooms where rooms.convent_id=game_entities.convent_id)
        from game_entities
        group by
            game_entities.id
        ;
    """)
    results = res.fetchall()
    for data in results:
        conn.execute("""
            update game_entities set room_id=%d where id=%d
        """.strip() % (data[1], data[0]))

    op.alter_column('game_entities', 'room_id', nullable=False)


def downgrade():
    op.drop_column('game_entities', 'room_id')
