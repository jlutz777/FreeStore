"""Add fields to the customerfamily table indicating if they are a customer and/or volunteer

Revision ID: 33ee99c0fb8
Revises: 2eeb0ddd8f9
Create Date: 2016-05-27 15:21:00.183936

"""

# revision identifiers, used by Alembic.
revision = '33ee99c0fb8'
down_revision = '2eeb0ddd8f9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('customerfamily',
                  sa.Column('is_customer', sa.Boolean, nullable=False, server_default=sa.true()))
    op.add_column('customerfamily',
                  sa.Column('is_volunteer', sa.Boolean, nullable=False, server_default=sa.false()))


def downgrade():
    op.drop_column('customerfamily', 'is_customer')
    op.drop_column('customerfamily', 'is_volunteer')
