"""Add quantity to shopping items

Revision ID: 32ccd6db0955
Revises: 430dc4ed6dd6
Create Date: 2015-01-06 21:59:03.761529

"""

# revision identifiers, used by Alembic.
revision = '32ccd6db0955'
down_revision = '430dc4ed6dd6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('shopping_item',
                  sa.Column('quantity', sa.Integer))


def downgrade():
    op.drop_column('shopping_item', 'quantity')

