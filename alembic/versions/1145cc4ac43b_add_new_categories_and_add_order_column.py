"""Add new categories and add order column

Revision ID: 1145cc4ac43b
Revises: 2a1c7cc1743b
Create Date: 2015-01-26 20:39:32.921622

"""

# revision identifiers, used by Alembic.
revision = '1145cc4ac43b'
down_revision = '2a1c7cc1743b'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table


def upgrade():
    op.add_column('shopping_category',
                  sa.Column('order', sa.Integer))

    shopping_categories = table(
        'shopping_category',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(75), nullable=False),
        sa.Column('daily_limit', sa.Integer, nullable=True),
        sa.Column('monthly_limit', sa.Integer, nullable=False),
        sa.Column('family_wide', sa.Boolean, nullable=False),
        sa.Column('order', sa.Integer, nullable=False)
    )

    op.bulk_insert(
        shopping_categories,
        [
            {'id': 7, 'name': 'Accessories',
                'daily_limit': 2, 'monthly_limit': 8,
                'family_wide': False,
                'order': 3},
            {'id': 8, 'name': 'Socks/Underwear',
                'daily_limit': 1, 'monthly_limit': 4,
                'family_wide': False,
                'order': 5},
            {'id': 9, 'name': 'Toys',
                'daily_limit': 1, 'monthly_limit': 4,
                'family_wide': False,
                'order': 6},
            {'id': 10, 'name': 'Books',
                'daily_limit': 2, 'monthly_limit': 8,
                'family_wide': False,
                'order': 7},
            {'id': 11, 'name': 'Seasonal',
                'daily_limit': 1, 'monthly_limit': 4,
                'family_wide': False,
                'order': 9},
        ])

    op.execute(
        shopping_categories.update().
        where(shopping_categories.c.name == op.inline_literal('Clothing')).
        values({'order': op.inline_literal('1')})
        )

    op.execute(
        shopping_categories.update().
        where(shopping_categories.c.name == op.inline_literal('Household')).
        values({'order': op.inline_literal('2'),
                'daily_limit': op.inline_literal('2'),
                'monthly_limit': op.inline_literal('2')})
        )

    op.execute(
        shopping_categories.update().
        where(shopping_categories.c.name == op.inline_literal('Shoes')).
        values({'order': op.inline_literal('4'),
                'daily_limit': op.inline_literal('1'),
                'monthly_limit': op.inline_literal('4')})
        )

    op.execute(
        shopping_categories.update().
        where(shopping_categories.c.name == op.inline_literal('Baby')).
        values({'order': op.inline_literal('8'),
                'daily_limit': op.inline_literal('1'),
                'monthly_limit': op.inline_literal('4')})
        )

    op.execute(
        shopping_categories.delete().
        where(shopping_categories.c.name == op.inline_literal('Coats'))
        )

    op.execute(
        shopping_categories.delete().
        where(shopping_categories.c.name == op.inline_literal('Other'))
        )


def downgrade():
    pass
