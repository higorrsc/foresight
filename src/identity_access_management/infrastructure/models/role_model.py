from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from src.shared_kernel.infrastructure.config import Base, GUID_Type

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column(
        "user_id",
        GUID_Type,
        ForeignKey("users.id"),
        primary_key=True,
    ),
    Column(
        "role_id",
        GUID_Type,
        ForeignKey("roles.id"),
        primary_key=True,
    ),
)


class RoleModel(Base):
    """
    SQLAlchemy model for the Role entity.
    """

    __tablename__ = "roles"

    id = Column(
        GUID_Type,
        primary_key=True,
        default=uuid4,
    )
    name = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )
    description = Column(
        String,
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

    users = relationship(
        "UserModel",
        secondary=user_roles,
        back_populates="roles",
    )

    permissions = relationship(
        "PermissionModel",
        secondary="role_permissions",
        back_populates="roles",
    )
