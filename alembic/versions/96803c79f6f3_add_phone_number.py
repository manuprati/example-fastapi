"""add phone number

Revision ID: 96803c79f6f3
Revises: 789f48abcedb
Create Date: 2022-07-26 15:07:35.465442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96803c79f6f3'
down_revision = '789f48abcedb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('votes', sa.Column('phone_number', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('votes', 'phone_number')
    # ### end Alembic commands ###
