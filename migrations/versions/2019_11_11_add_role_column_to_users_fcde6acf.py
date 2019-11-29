"""add role column to users

Revision ID: 5554fcde6acf
Revises: 3e9e9333b5bc
Create Date: 2019-11-11 17:34:09.014104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5554fcde6acf'
down_revision = '3e9e9333b5bc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('role', sa.Integer, default=0))


def downgrade():
    op.drop_column('users', 'role')
