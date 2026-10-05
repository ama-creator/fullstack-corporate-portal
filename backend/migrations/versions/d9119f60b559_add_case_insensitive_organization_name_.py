"""add case insensitive organization name indexes

Revision ID: d9119f60b559
Revises: 84eabb560677
Create Date: 2026-10-05 13:16:06.681278

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9119f60b559'
down_revision: Union[str, Sequence[str], None] = '84eabb560677'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "uq_departments_name_lower",
        "departments",
        [sa.text("lower(name)")],
        unique=True,
    )

    op.create_index(
        "uq_positions_name_lower",
        "positions",
        [sa.text("lower(name)")],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        "uq_positions_name_lower",
        table_name="positions",
    )

    op.drop_index(
        "uq_departments_name_lower",
        table_name="departments",
    )
