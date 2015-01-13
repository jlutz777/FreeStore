"""Add shopping item to dependent relationship and remove name

Revision ID: 2662d94ed399
Revises: 32ccd6db0955
Create Date: 2015-01-10 15:02:31.721598

"""

# revision identifiers, used by Alembic.
revision = '2662d94ed399'
down_revision = '32ccd6db0955'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('shopping_item', sa.Column('dependent',
                  sa.Integer, sa.ForeignKey('dependents.id')))
    op.drop_column('shopping_item', 'name')


def downgrade():
    op.drop_column('shopping_item', 'dependent')
    op.add_column('shopping_item',
                  sa.Column('name', sa.Unicode(75), nullable=True))
