"""Make checkout column optional

Revision ID: 334d0fe3706d
Revises: 3838ebd18fd9
Create Date: 2014-11-24 16:46:42.006635

"""

# revision identifiers, used by Alembic.
revision = '334d0fe3706d'
down_revision = '3838ebd18fd9'

from alembic import op


def upgrade():
	op.alter_column('visits', 'checkout', nullable=True)


def downgrade():
    op.alter_column('visits', 'checkout', nullable=False)
