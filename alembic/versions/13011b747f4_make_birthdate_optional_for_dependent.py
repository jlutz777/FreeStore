"""Make birthdate optional for dependent

Revision ID: 13011b747f4
Revises: ffb0d8f956
Create Date: 2016-06-16 12:43:31.028641

"""

# revision identifiers, used by Alembic.
revision = '13011b747f4'
down_revision = 'ffb0d8f956'

from alembic import op
import sqlalchemy as sa


def upgrade():
	op.alter_column('dependents', 'birthdate', nullable=True)


def downgrade():
    op.alter_column('dependents', 'birthdate', nullable=False)
