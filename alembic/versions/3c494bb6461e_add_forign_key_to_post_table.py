"""add forign key to post table

Revision ID: 3c494bb6461e
Revises: a7ee19320bf5
Create Date: 2022-07-26 11:15:02.678163

"""
from tkinter import CASCADE
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c494bb6461e'
down_revision = 'a7ee19320bf5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("post_user_fk", source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE" )
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name='posts')
    op.drop_column('posts', column_name='owner_id')
    pass
