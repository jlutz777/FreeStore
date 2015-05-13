"""Add checkout comment

Revision ID: 219e163cd6e
Revises: 26969f150b46
Create Date: 2015-05-13 07:40:04.859096

"""

# revision identifiers, used by Alembic.
revision = '219e163cd6e'
down_revision = '26969f150b46'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('customerfamily',
                  sa.Column('checkoutcomments', sa.Unicode(250)))


def downgrade():
    op.drop_column('customerfamily', 'checkoutcomments')
