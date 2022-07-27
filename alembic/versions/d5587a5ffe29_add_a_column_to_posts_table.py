"""add a column to  posts table

Revision ID: d5587a5ffe29
Revises: ca97da75f8f5
Create Date: 2022-07-25 17:03:21.390642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5587a5ffe29'
down_revision = 'ca97da75f8f5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('title', sa.String(), nullable=False ))
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False ))


def downgrade() -> None:
    op.drop_column('posts','title')
    op.drop_column('posts','content')
    pass
