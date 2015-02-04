"""Add age and disabled columns to category table

Revision ID: 2eb054267c19
Revises: 1145cc4ac43b
Create Date: 2015-02-01 20:37:41.995995

"""

# revision identifiers, used by Alembic.
revision = '2eb054267c19'
down_revision = '1145cc4ac43b'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table


def upgrade():
    op.add_column('shopping_category',
                  sa.Column('disabled', sa.Boolean))
    op.add_column('shopping_category',
                  sa.Column('min_age', sa.Integer))
    op.add_column('shopping_category',
                  sa.Column('max_age', sa.Integer))

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

    op.execute(
        shopping_categories.update().
        values({'disabled': op.inline_literal(False)})
        )

    op.execute(
        shopping_categories.update().
        where(shopping_categories.c.name == op.inline_literal('Baby')).
        values({'min_age': op.inline_literal('0'),
                'max_age': op.inline_literal('2')})
        )

    op.execute(
        shopping_categories.update().
        where(shopping_categories.c.name == op.inline_literal('Books')).
        values({'min_age': op.inline_literal('0'),
                'max_age': op.inline_literal('16')})
        )

    op.execute(
        shopping_categories.update().
        where(shopping_categories.c.name == op.inline_literal('Toys')).
        values({'min_age': op.inline_literal('0'),
                'max_age': op.inline_literal('16')})
        )


def downgrade():
    op.drop_column('shopping_category', 'disabled')
    op.drop_column('shopping_category', 'min_age')
    op.drop_column('shopping_category', 'max_age')
