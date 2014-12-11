"""Add reference between visit and items

Revision ID: 3a1dddd0c0f8
Revises: 334d0fe3706d
Create Date: 2014-12-11 08:49:03.268514

"""

# revision identifiers, used by Alembic.
revision = '3a1dddd0c0f8'
down_revision = '334d0fe3706d'

from alembic import op
import sqlalchemy as sa

def upgrade():
	op.add_column('shopping_item',
		sa.Column('visit', sa.Integer, sa.ForeignKey('visits.id')))

def downgrade():
    op.drop_column('shopping_item', 'visit')
