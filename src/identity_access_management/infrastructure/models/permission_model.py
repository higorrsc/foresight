from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from src.shared_kernel.infrastructure.config import Base, GUID_Type

user_permissions = Table(
    "user_permissions",
    Base.metadata,
    Column(
        "user_id",
        GUID_Type,
        ForeignKey("users.id"),
        primary_key=True,
    ),
    Column(
        "permission_id",
        GUID_Type,
        ForeignKey("permissions.id"),
        primary_key=True,
    ),
)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column(
        "role_id",
        GUID_Type,
        ForeignKey("roles.id"),
        primary_key=True,
    ),
    Column(
        "permission_id",
        GUID_Type,
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
        GUID_Type,
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
