"""Added file_name and file_url to Todo

Revision ID: 43c36c063ae2
Revises:
Create Date: 2024-09-10 13:49:10.333223

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "43c36c063ae2"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("todo", sa.Column("file_name", sa.String(), nullable=True))
    op.add_column("todo", sa.Column("file_url", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("todo", "file_name")
    op.drop_column("todo", "file_url")
