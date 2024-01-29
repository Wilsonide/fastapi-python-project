"""add user table

Revision ID: ffb0c917eed4
Revises: 3208532acb04
Create Date: 2024-01-29 07:33:44.721368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffb0c917eed4'
down_revision: Union[str, None] = '7e28dc0a8a02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
    sa.Column("id", sa.Integer(), primary_key=True,nullable=False), 
    sa.Column("email", sa.String(), nullable=False), 
    sa.Column("password", sa.String(), nullable=False), 
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()"))
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
