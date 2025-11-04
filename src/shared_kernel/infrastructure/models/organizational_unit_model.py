from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from src.shared_kernel.infrastructure.config import Base, GUID_Type


class OrganizationalUnitModel(Base):
    """
    SQLAlchemy model for the OrganizationalUnit entity.
    """

    __tablename__ = "organizational_units"

    id = Column(
        GUID_Type,
        primary_key=True,
        default=uuid4,
    )
    tenant_id = Column(
        GUID_Type,
        ForeignKey("tenants.id"),
        nullable=False,
        index=True,
    )
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
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
    )
    created_at = Column(
        DateTime,
        default=datetime.now,
    )
    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )
    deleted_at = Column(
        DateTime,
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
