"""fill_with_smg_users

Revision ID: bfae164c49e1
Revises: 826c7c10d5ec
Create Date: 2019-11-20 12:43:50.344750

"""
from typing import List

from alembic import op
import sqlalchemy as sa

import settings
from database.models import User
from loop import event_loop

revision = 'bfae164c49e1'
down_revision = '826c7c10d5ec'
branch_labels = None
depends_on = None


connection = op.get_bind()


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(), nullable=False))
    op.drop_constraint('users_chat_id_key', 'users', type_='unique')
    op.create_unique_constraint('users_email_key', 'users', ['email'])
    op.drop_column('users', 'chat_id')
    # ### end Alembic commands ###


def downgrade():
    op.drop_constraint('users_email_key', 'users', type_='unique')
    op.drop_column('users', 'email')

    op.add_column('users', sa.Column('chat_id', sa.CHAR(length=100),
                                     autoincrement=False, nullable=False))
    op.create_unique_constraint('users_chat_id_key', 'users', ['chat_id'])

