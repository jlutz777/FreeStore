"""add winter seasonal category

Revision ID: 2eeb0ddd8f9
Revises: 14b52358eb42
Create Date: 2015-10-16 00:50:15.154646

"""

# revision identifiers, used by Alembic.
revision = '2eeb0ddd8f9'
down_revision = '14b52358eb42'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table


def upgrade():
    shopping_categories = table(
        'shopping_category',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(75), nullable=False),
        sa.Column('daily_limit', sa.Integer, nullable=True),
        sa.Column('monthly_limit', sa.Integer, nullable=False),
        sa.Column('family_wide', sa.Boolean, nullable=False),
        sa.Column('order', sa.Integer, nullable=False),
        sa.Column('min_age', sa.Integer, nullable=True),
        sa.Column('max_age', sa.Integer, nullable=True),
        sa.Column('disabled', sa.Boolean, nullable=False)
    )
    
    op.bulk_insert(
        shopping_categories,
        [
            {'id': 12, 'name': 'Winter Seasonal',
                'daily_limit': 1, 'monthly_limit': 4,
                'family_wide': False,
                'order': 9, 'disabled': False}
        ])

    op.execute(
        shopping_categories.update().
        where(shopping_categories.c.name == op.inline_literal('Seasonal')).
        values({'disabled': op.inline_literal(True)})
        )


def downgrade():
    pass
