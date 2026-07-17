from sqlalchemy import Column, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import relationship

from src.core.infrastructure.config import GUIDType, SQLAlchemyBase
from src.core.infrastructure.config.mixins import (
    SQLAlchemySoftDeletableMixin,
    SQLAlchemyTenantMixin,
    SQLAlchemyUserAuditMixin,
)


class OrganizationalUnitModel(
    SQLAlchemyBase,
    SQLAlchemySoftDeletableMixin,
    SQLAlchemyTenantMixin,
    SQLAlchemyUserAuditMixin,
):
    """
    SQLAlchemy model for the OrganizationalUnit entity.
    """

    __tablename__ = "organizational_units"

    code = Column(
        String(100),
        nullable=False,
    )
    description = Column(
        String(100),
        nullable=False,
    )
    parent_id = Column(
        GUIDType,
        ForeignKey("organizational_units.id"),
        nullable=True,
    )

    parent = relationship(
        "OrganizationalUnitModel",
        foreign_keys=[parent_id],
        remote_side="OrganizationalUnitModel.id",
        back_populates="children",
    )

    children = relationship(
        "OrganizationalUnitModel",
        back_populates="parent",
    )

    __table_args__ = (
        UniqueConstraint(
            "code",
            "tenant_id",
        ),
        Index(
            "idx_org_units_parent_tenant",
            "parent_id",
            "tenant_id",
        ),
    )
