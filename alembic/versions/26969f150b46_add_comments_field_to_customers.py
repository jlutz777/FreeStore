"""Add comments field to customers

Revision ID: 26969f150b46
Revises: 2eb054267c19
Create Date: 2015-03-17 21:38:50.147724

"""

# revision identifiers, used by Alembic.
revision = '26969f150b46'
down_revision = '2eb054267c19'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('customerfamily',
                  sa.Column('comments', sa.Unicode(200)))


def downgrade():
    op.drop_column('customerfamily', 'comments')
