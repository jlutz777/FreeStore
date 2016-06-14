"""Add volunter visit table

Revision ID: ffb0d8f956
Revises: 33ee99c0fb8
Create Date: 2016-05-27 20:32:57.396307

"""

# revision identifiers, used by Alembic.
revision = 'ffb0d8f956'
down_revision = '33ee99c0fb8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'volunteervisits',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('checkin', sa.DateTime, nullable=True),
        sa.Column('checkout', sa.DateTime, nullable=True),
        sa.Column('family', sa.Integer, sa.ForeignKey('customerfamily.id'))
    )


def downgrade():
    op.drop_table('volunteervisits')
