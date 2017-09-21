"""Add GameBorrow models

Revision ID: 1c6eaf90111
Revises: fc6deff112
Create Date: 2014-08-25 20:09:28.734963

"""

# revision identifiers, used by Alembic.
revision = '1c6eaf90111'
down_revision = 'fc6deff112'

from datetime import datetime
from alembic import op
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean


def upgrade():
    op.create_table(
        'game_borrows',
        Column(
            'id',
            Integer,
            primary_key=True),

        Column(
            'game_entity_id',
            Integer,
            ForeignKey('game_entities.id'),
            nullable=False),
        Column(
            'borrowed_timestamp',
            DateTime,
            default=datetime.now,
            nullable=False),
        Column(
            'return_timestamp',
            DateTime),
        Column(
            'is_borrowed',
            Boolean),

        Column(
            'name',
            String),
        Column(
            'surname',
            String),
        Column(
            'document_type',
            String),
        Column(
            'document_number',
            String),
    )


def downgrade():
    op.drop_table('game_borrows')
