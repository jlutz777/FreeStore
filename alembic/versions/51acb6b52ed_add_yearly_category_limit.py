"""Add yearly category limit

Revision ID: 51acb6b52ed
Revises: 13011b747f4
Create Date: 2016-10-21 00:22:16.102929

"""

# revision identifiers, used by Alembic.
revision = '51acb6b52ed'
down_revision = '13011b747f4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('shopping_category',
                  sa.Column('yearly_limit', sa.Integer))


def downgrade():
    op.drop_column('shopping_category', 'yearly_limit')

