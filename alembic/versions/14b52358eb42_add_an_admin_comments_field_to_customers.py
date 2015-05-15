"""Add an admin comments field to customers

Revision ID: 14b52358eb42
Revises: 219e163cd6e
Create Date: 2015-05-14 21:19:07.814989

"""

# revision identifiers, used by Alembic.
revision = '14b52358eb42'
down_revision = '219e163cd6e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('customerfamily',
                  sa.Column('admincomments', sa.Unicode(250)))


def downgrade():
    op.drop_column('customerfamily', 'admincomments')
