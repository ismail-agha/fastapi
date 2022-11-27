"""add content column to post table

Revision ID: 80a28ca913a6
Revises: a50023d571a1
Create Date: 2022-11-27 13:49:36.360817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80a28ca913a6'
down_revision = 'a50023d571a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
