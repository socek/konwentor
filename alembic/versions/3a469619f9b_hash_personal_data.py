"""hash_personal_data

Revision ID: 3a469619f9b
Revises: 16de96e7f7a
Create Date: 2014-11-30 15:16:04.871953

"""

# revision identifiers, used by Alembic.
revision = '3a469619f9b'
down_revision = '16de96e7f7a'

from alembic import op
from sqlalchemy import Column, String
from hashlib import sha224
from konwentor.application.init import main


def hash_document(document, number):
    seed = main.settings['personal_seed']
    data = bytes(seed + document + number, encoding='utf8')
    return sha224(data).hexdigest()


def upgrade():
    op.add_column(
        'game_borrows',
        Column(
            'stats_hash',
            String,
            nullable=False,
            server_default='xxx'))
    connection = op.get_bind()
    sql = 'select id, document_type, document_number from game_borrows;'
    pending_sql = ''
    for result in connection.execute(sql).fetchall():
        hashed = hash_document(
            result['document_type'],
            result['document_number'])
        pending_sql += (
            'update game_borrows set stats_hash=\'{0}\' where id={1};'.format(
                hashed, result[0])
        )
    if pending_sql != '':
        connection.execute(pending_sql)

    op.drop_column('game_borrows', 'document_type')
    op.drop_column('game_borrows', 'document_number')
    op.alter_column('game_borrows', 'game_borrows', new_column_name='name')


def downgrade():
    pass
