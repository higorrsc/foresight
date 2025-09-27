from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, String

from src.core.infrastructure.config.database import Base


class UserModel(Base):
    """
    SQLAlchemy model for the User entity.
    """

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    username = Column(
        String(50),
        unique=True,
        nullable=False,
    )
    password = Column(
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
