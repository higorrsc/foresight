from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, String

from src.shared_kernel.infrastructure.config import Base, GUID_Type


class AreaModel(Base):
    """
    SQLAlchemy model for the Area entity.
    """

    __tablename__ = "areas"

    id = Column(
        GUID_Type,
        primary_key=True,
        default=uuid4,
    )
    description = Column(
        String(100),
        nullable=False,
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
