from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, String

from src.core.infrastructure.config.database import Base


class AreaModel(Base):
    """
    SQLAlchemy model for the Area entity.
    """

    __tablename__ = "areas"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    description = Column(
        String(100),
        nullable=False,
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
