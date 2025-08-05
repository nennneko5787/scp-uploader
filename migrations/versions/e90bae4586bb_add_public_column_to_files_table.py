"""Add public column to files table

Revision ID: e90bae4586bb
Revises: 412f4ec70591
Create Date: 2025-08-05 10:44:59.183150

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e90bae4586bb"
down_revision: Union[str, Sequence[str], None] = "412f4ec70591"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "files",
        sa.Column("public", sa.Boolean(), nullable=False, server_default="true"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("files", "public")
