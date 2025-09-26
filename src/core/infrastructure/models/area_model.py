from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AreaModel(Base):
    """
    SQLAlchemy model for the Area entity.
    """

    __tablename__ = "areas"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
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
