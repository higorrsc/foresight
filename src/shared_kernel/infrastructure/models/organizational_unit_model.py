from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from src.shared_kernel.infrastructure.config import GUID_Type, SQLAlchemyBase
from src.shared_kernel.infrastructure.models._shared.mixins import (
    SQLAlchemySoftDeletableMixin,
    SQLAlchemyTenantMixin,
)


class OrganizationalUnitModel(
    SQLAlchemyBase,
    SQLAlchemyTenantMixin,
    SQLAlchemySoftDeletableMixin,
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
        remote_side=[id],
        back_populates="children",
    )

    children = relationship(
        "OrganizationalUnitModel",
        back_populates="parent",
    )
