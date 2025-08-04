"""Create files table

Revision ID: 412f4ec70591
Revises: 5d383f2726b1
Create Date: 2025-08-04 16:06:33.101953

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "412f4ec70591"
down_revision: Union[str, Sequence[str], None] = "5d383f2726b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "files",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column(
            "created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("edited_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("author_id", sa.VARCHAR(), nullable=False),
        sa.Column("name", sa.String(60), nullable=False),
        sa.Column("description", sa.String(600), nullable=False),
        sa.Column(
            "tags", sa.ARRAY(sa.VARCHAR(60)), nullable=False, server_default="{}"
        ),
        sa.Column("title", sa.String(60), nullable=False),
        sa.Column("size", sa.Float(), nullable=False),
        sa.Column("views", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("downloads", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("files")
