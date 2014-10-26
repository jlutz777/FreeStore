"""Add cork tables

Revision ID: 39675efc6d59
Revises: 3053811d54d4
Create Date: 2014-10-26 02:10:19.454966

"""

# revision identifiers, used by Alembic.
revision = '39675efc6d59'
down_revision = '3053811d54d4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'roles',
        sa.Column('role', sa.String(128), primary_key=True),
        sa.Column('level', sa.Integer, nullable=False)
        )
    op.create_table(
        'users',
        sa.Column('username', sa.String(128), primary_key=True),
        sa.Column('role', sa.ForeignKey('roles.role')),
        sa.Column('hash', sa.String(256), nullable=False),
        sa.Column('email_addr', sa.String(128)),
        sa.Column('desc', sa.String(128)),
        sa.Column('creation_date', sa.String(128), nullable=False),
        sa.Column('last_login', sa.String(128), nullable=False)
        )
    op.create_table(
        'register',
        sa.Column('code', sa.String(128), primary_key=True),
        sa.Column('username', sa.String(128), nullable=False),
        sa.Column('role', sa.ForeignKey('roles.role')),
        sa.Column('hash', sa.String(256), nullable=False),
        sa.Column('email_addr', sa.String(128)),
        sa.Column('desc', sa.String(128)),
        sa.Column('creation_date', sa.String(128), nullable=False)
        )
        

def downgrade():
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('register')
