from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from src.shared_kernel.infrastructure.config import Base

user_permissions = Table(
    "user_permissions",
    Base.metadata,
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
    ),
    Column(
        "permission_id",
        UUID(as_uuid=True),
        ForeignKey("permissions.id"),
        primary_key=True,
    ),
)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column(
        "role_id",
        UUID(as_uuid=True),
        ForeignKey("roles.id"),
        primary_key=True,
    ),
    Column(
        "permission_id",
        UUID(as_uuid=True),
        ForeignKey("permissions.id"),
        primary_key=True,
    ),
)


class PermissionModel(Base):
    """
    SQLAlchemy model for the Permission entity.
    """

    __tablename__ = "permissions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    codename = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )
    description = Column(
        String,
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

    users = relationship(
        "UserModel",
        secondary=user_permissions,
        back_populates="permissions",
    )

    roles = relationship(
        "RoleModel",
        secondary=role_permissions,
        back_populates="permissions",
    )
