"""create users table

Revision ID: 3e9e9333b5bc
Revises: 
Create Date: 2019-11-11 11:54:18.671076

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3e9e9333b5bc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("skype_id", sa.CHAR(100), unique=True, nullable=False),
                    sa.Column("chat_id", sa.CHAR(100), unique=True, nullable=False),
                    sa.Column("skype_display_name", sa.CHAR(100), nullable=True),
                    )


def downgrade():
    op.drop_table('users')
