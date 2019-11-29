"""add_first_last_name

Revision ID: 826c7c10d5ec
Revises: 5554fcde6acf
Create Date: 2019-11-14 17:03:48.074972

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '826c7c10d5ec'
down_revision = '5554fcde6acf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('first_name', sa.String(), nullable=False))
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=True))
    op.drop_column('users', 'skype_display_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('skype_display_name', sa.CHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    # ### end Alembic commands ###
