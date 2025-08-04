"""Create users table

Revision ID: 5d383f2726b1
Revises:
Create Date: 2025-08-04 09:53:06.789744

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5d383f2726b1"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.VARCHAR(), primary_key=True),
        sa.Column("handle", sa.VARCHAR(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("about_me", sa.String(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
