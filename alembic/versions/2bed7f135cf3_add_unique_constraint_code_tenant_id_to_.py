"""add unique constraint code_tenant_id to org_units

Revision ID: 2bed7f135cf3
Revises: 3c06c5788579
Create Date: 2025-12-08 18:48:41.191735

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2bed7f135cf3"
down_revision: str | Sequence[str] | None = "3c06c5788579"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    if bind.dialect.name == "sqlite":
        with op.batch_alter_table("organizational_units", schema=None) as batch_op:
            batch_op.create_unique_constraint(
                "uq_organizational_units_code",
                ["code", "tenant_id"],
            )
    else:
        # Create unique index concurrently first to avoid table locks
        with op.get_context().autocommit_block():
            op.create_index(
                "uq_organizational_units_code_idx",
                "organizational_units",
                ["code", "tenant_id"],
                unique=True,
                postgresql_concurrently=True,
            )
        # Create constraint using the index
        op.create_unique_constraint(
            "uq_organizational_units_code",
            "organizational_units",
            ["code", "tenant_id"],
            postgresql_using_index="uq_organizational_units_code_idx",
        )


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    if bind.dialect.name == "sqlite":
        with op.batch_alter_table("organizational_units", schema=None) as batch_op:
            batch_op.drop_constraint(
                "uq_organizational_units_code",
                type_="unique",
            )
    else:
        op.drop_constraint(
            "uq_organizational_units_code",
            "organizational_units",
            type_="unique",
        )
        # Drop the unique index concurrently
        with op.get_context().autocommit_block():
            op.drop_index(
                "uq_organizational_units_code_idx",
                table_name="organizational_units",
                postgresql_concurrently=True,
            )
