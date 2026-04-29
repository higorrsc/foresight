from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import declarative_mixin, declared_attr, relationship

from src.core.infrastructure.config import GUID_Type


@declarative_mixin
class SQLAlchemyTenantMixin:
    """
    Tenant mixin for SQLAlchemy models.
    """

    @declared_attr
    def tenant_id(cls):  # pylint: disable=E0213
        """
        Add TenantID field.
        """

        return Column(
            GUID_Type,
            ForeignKey("tenants.id"),
            nullable=False,
            index=True,
        )

    @declared_attr
    def tenant(cls):  # pylint: disable=E0213
        """
        Add TenantModel relationship.
        """

        return relationship(
            "TenantModel",
            foreign_keys=[cls.tenant_id],
            lazy="joined",
        )
