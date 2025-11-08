from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from src.shared_kernel.infrastructure.config import (
    GUID_Type,
    SQLAlchemyBase,
    SQLAlchemySoftDeletableMixin,
    SQLAlchemyTenantMixin,
    SQLAlchemyUserAuditFields,
)


class OrganizationalUnitModel(
    SQLAlchemyBase,
    SQLAlchemySoftDeletableMixin,
    SQLAlchemyTenantMixin,
    SQLAlchemyUserAuditFields,
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
        GUID_Type,
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
