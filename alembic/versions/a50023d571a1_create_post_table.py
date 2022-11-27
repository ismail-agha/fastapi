"""create post table

Revision ID: a50023d571a1
Revises: 
Create Date: 2022-11-27 12:47:33.556751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a50023d571a1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                                sa.Column('title', sa.String(), nullable=False)   )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
