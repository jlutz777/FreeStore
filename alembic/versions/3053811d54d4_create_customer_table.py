"""create customer table

Revision ID: 3053811d54d4
Revises: None
Create Date: 2014-10-21 01:55:38.839643

"""

# revision identifiers, used by Alembic.
revision = '3053811d54d4'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'customerfamily',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.Unicode(100), nullable=False),
        sa.Column('phone', sa.Unicode(40)),
        sa.Column('address', sa.Unicode(100), nullable=False),
        sa.Column('city', sa.Unicode(40), nullable=False),
        sa.Column('state', sa.Unicode(40), nullable=False),
        sa.Column('zip', sa.Unicode(20), nullable=False),
        sa.Column('datecreated', sa.DateTime, nullable=False)
    )


def downgrade():
    op.drop_table('customerfamily')
