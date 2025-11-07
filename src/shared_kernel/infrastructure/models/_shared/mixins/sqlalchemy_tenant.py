from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import declared_attr, relationship

from src.shared_kernel.infrastructure.config.custom_types import GUID_Type


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
