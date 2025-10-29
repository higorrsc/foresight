from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from src.shared_kernel.infrastructure.config import Base


class OrganizationalUnitModel(Base):
    """
    SQLAlchemy model for the OrganizationalUnit entity.
    """

    __tablename__ = "organizational_units"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
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
        UUID(as_uuid=True),
        ForeignKey("organizational_units.id"),
        nullable=False,
    )
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
    )
    deleted_at = Column(
        DateTime,
        nullable=True,
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

    parent = relationship(
        "OrganizationalUnitModel",
        remote_side=[id],
        back_populates="children",
    )
    children = relationship(
        "OrganizationalUnitModel",
        back_populates="parent",
    )
