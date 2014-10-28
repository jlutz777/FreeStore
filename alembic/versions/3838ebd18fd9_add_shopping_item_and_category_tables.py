"""Add shopping item and category tables

Revision ID: 3838ebd18fd9
Revises: 44ef82f9b572
Create Date: 2014-10-28 02:41:51.027397

"""

# revision identifiers, used by Alembic.
revision = '3838ebd18fd9'
down_revision = '44ef82f9b572'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'shopping_category',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(75), nullable=False),
        sa.Column('daily_limit', sa.Integer, nullable=True)
    )
    op.create_table(
        'shopping_item',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(75), nullable=False),
        sa.Column('category', sa.Integer, sa.ForeignKey('shopping_category.id'))
    )


def downgrade():
    op.drop_table('shopping_category')
    op.drop_table('shopping_item')
