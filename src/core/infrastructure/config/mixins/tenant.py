from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import declarative_mixin, declared_attr, relationship

from src.core.infrastructure.config import GUIDType


@declarative_mixin
class SQLAlchemyTenantMixin:
    """
    Tenant mixin for SQLAlchemy models.
    """

    @declared_attr
    def tenant_id(cls):  # noqa: N805
        """
        Add TenantID field.
        """

        return Column(
            GUIDType,
            ForeignKey("tenants.id"),
            nullable=False,
            index=True,
        )

    @declared_attr
    def tenant(cls):  # noqa: N805
        """
        Add TenantModel relationship.
        """

        return relationship(
            "TenantModel",
            foreign_keys=[cls.tenant_id],
        )
