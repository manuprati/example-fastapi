"""create users table

Revision ID: a7ee19320bf5
Revises: d5587a5ffe29
Create Date: 2022-07-25 17:13:34.044180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7ee19320bf5'
down_revision = 'd5587a5ffe29'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',sa.Column('id',sa.Integer(), nullable=False),
                            sa.Column('email',sa.String(), nullable=False),
                            sa.Column('password',sa.String(),  nullable=False),
                            sa.Column('created_At',sa.TIMESTAMP(timezone=True), 
                            server_default=sa.text('now()'), nullable=False),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
