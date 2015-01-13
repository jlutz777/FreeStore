"""Add monthly limit to categories

Revision ID: 2a1c7cc1743b
Revises: 2662d94ed399
Create Date: 2015-01-10 15:19:06.084824

"""

# revision identifiers, used by Alembic.
revision = '2a1c7cc1743b'
down_revision = '2662d94ed399'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('shopping_category',
                  sa.Column('monthly_limit', sa.Integer))
    op.add_column('shopping_category',
                  sa.Column('family_wide', sa.Boolean))


def downgrade():
    op.drop_column('shopping_category', 'monthly_limit')
    op.drop_column('shopping_category', 'family_wide')
