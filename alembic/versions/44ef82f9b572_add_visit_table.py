"""Add visit table

Revision ID: 44ef82f9b572
Revises: 486cb2b8cb8f
Create Date: 2014-10-28 02:34:33.824605

"""

# revision identifiers, used by Alembic.
revision = '44ef82f9b572'
down_revision = '486cb2b8cb8f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'visits',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('checkin', sa.DateTime, nullable=False),
        sa.Column('checkout', sa.DateTime, nullable=False),
        sa.Column('family', sa.Integer, sa.ForeignKey('customerfamily.id'))
    )


def downgrade():
    op.drop_table('visits')
