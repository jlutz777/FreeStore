"""Add shopping categories

Revision ID: 430dc4ed6dd6
Revises: 3a1dddd0c0f8
Create Date: 2014-12-24 09:55:10.993854

"""

# revision identifiers, used by Alembic.
revision = '430dc4ed6dd6'
down_revision = '3a1dddd0c0f8'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table


def upgrade():
    shopping_categories = table(
        'shopping_category',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(75), nullable=False),
        sa.Column('daily_limit', sa.Integer, nullable=True)
    )

    op.bulk_insert(
        shopping_categories,
        [
            {'id': 1, 'name': 'Clothing',
                'daily_limit': 5},
            {'id': 2, 'name': 'Household',
                'daily_limit': 5},
            {'id': 3, 'name': 'Shoes',
                'daily_limit': 5},
            {'id': 4, 'name': 'Baby',
                'daily_limit': 5},
            {'id': 5, 'name': 'Coats',
                'daily_limit': 5},
            {'id': 6, 'name': 'Other',
                'daily_limit': 5}
        ])


def downgrade():
    pass
