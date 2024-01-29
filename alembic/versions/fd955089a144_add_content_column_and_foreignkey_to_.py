"""add content column and foreignkey to post table

Revision ID: fd955089a144
Revises: ffb0c917eed4
Create Date: 2024-01-29 07:56:33.433617

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd955089a144'
down_revision: Union[str, None] = 'ffb0c917eed4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", 
    sa.Column("content", sa.String(), nullable=False)
    )

    op.add_column("posts", 
    sa.Column("owner_id", sa.Integer(), nullable=False)
    )

    op.create_foreign_key("post_users_fk",source_table="posts", referent_table="users",local_cols=["owner_id"], remote_cols=["id"], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    op.drop_constraint("post_users_fk",table_name="posts")
    op.add_column("posts","owner_id")
    pass
