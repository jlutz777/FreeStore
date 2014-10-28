"""Add dependents

Revision ID: 486cb2b8cb8f
Revises: 39675efc6d59
Create Date: 2014-10-28 02:09:45.052665

"""

# revision identifiers, used by Alembic.
revision = '486cb2b8cb8f'
down_revision = '39675efc6d59'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'dependents',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('primary', sa.Boolean, nullable=False),
        sa.Column('first_name', sa.Unicode(50), nullable=False),
        sa.Column('last_name', sa.Unicode(50), nullable=False),
        sa.Column('birthdate', sa.DateTime, nullable=False),
        sa.Column('family', sa.Integer, sa.ForeignKey('customerfamily.id'))
    )


def downgrade():
    op.drop_table('dependents')
