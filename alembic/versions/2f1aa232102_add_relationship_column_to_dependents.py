"""Add relationship column to dependents

Revision ID: 2f1aa232102
Revises: 51acb6b52ed
Create Date: 2020-12-14 20:17:33.378756

"""

# revision identifiers, used by Alembic.
revision = '2f1aa232102'
down_revision = '51acb6b52ed'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table


def upgrade():
    op.create_table(
        'relationships',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(75), nullable=False)
    )
    
    relationships = table(
        'relationships',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(75), nullable=False)
    )
    
    op.bulk_insert(
        relationships,
        [
            {'id': 1, 'name': 'spouse/significant other'},
            {'id': 2, 'name': 'child'},
            {'id': 3, 'name': 'grandparent'},
            {'id': 4, 'name': 'grandchild'},
            {'id': 5, 'name': 'other'}
        ])

    op.add_column('dependents',
                  sa.Column('relationship', sa.Integer,\
                  sa.ForeignKey('relationships.id'), nullable=True))


def downgrade():
    op.drop_column('dependents', 'relationship')
    op.drop_table('relationships')
