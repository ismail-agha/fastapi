"""add frreign-key to posts table

Revision ID: d13cf15c37c8
Revises: e0a63ae8b8a5
Create Date: 2022-11-27 14:56:06.379108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd13cf15c37c8'
down_revision = 'e0a63ae8b8a5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk',
                          source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'],
                          ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
