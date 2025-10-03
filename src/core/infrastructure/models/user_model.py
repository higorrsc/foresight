from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship

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
    hashed_password = Column(
        String,
        nullable=False,
    )
    roles = relationship(
        "RoleModel",
        secondary="user_roles",
        back_populates="users",
        lazy="joined",
    )
    first_name = Column(
        String(100),
        nullable=True,
    )
    last_name = Column(
        String(100),
        nullable=True,
    )
    email = Column(
        String,
        nullable=True,
        unique=True,
        index=True,
    )
    is_active = Column(
        Boolean,
        default=True,
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
