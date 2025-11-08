from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Column, DateTime

from .base import Base
from .custom_types import GUID_Type


class SQLAlchemyBase(Base):
    """
    Base class for all SQLAlchemy models with common fields.

    Include common audit and identification fields:
        - id (UUID): Primary key.
        - created_at (datetime): Timestamp when the record was created.
        - updated_at (datetime): Timestamp when the record was last updated.
    """

    __abstract__ = True

    id = Column(
        GUID_Type,
        primary_key=True,
        default=uuid4,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
