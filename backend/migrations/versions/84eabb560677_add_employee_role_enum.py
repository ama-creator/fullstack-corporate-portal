"""add employee role enum

Revision ID: 84eabb560677
Revises: 0120b80ce000
Create Date: 2026-09-14 21:25:06.463127

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "84eabb560677"
down_revision: str | Sequence[str] | None = "0120b80ce000"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    employee_role = sa.Enum(
        "employee",
        "manager",
        "hr",
        "admin",
        name="employee_role",
    )

    employee_role.create(op.get_bind())

    op.alter_column(
        "employees",
        "role",
        existing_type=sa.VARCHAR(length=30),
        type_=employee_role,
        existing_nullable=False,
        postgresql_using="role::employee_role",
    )


def downgrade() -> None:
    op.alter_column(
        "employees",
        "role",
        existing_type=sa.Enum(
            "employee",
            "manager",
            "hr",
            "admin",
            name="employee_role",
        ),
        type_=sa.VARCHAR(length=30),
        existing_nullable=False,
    )

    sa.Enum(
        "employee",
        "manager",
        "hr",
        "admin",
        name="employee_role",
    ).drop(op.get_bind())
