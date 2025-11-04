from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from src.shared_kernel.infrastructure.config import Base, GUID_Type


class UserModel(Base):
    """
    SQLAlchemy model for the User entity.
    """

    __tablename__ = "users"

    id = Column(
        GUID_Type,
        primary_key=True,
        default=uuid4,
    )
    tenant_id = Column(
        GUID_Type,
        ForeignKey("tenants.id"),
        nullable=True,
        index=True,
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

    roles = relationship(
        "RoleModel",
        secondary="user_roles",
        back_populates="users",
        lazy="joined",
    )

    permissions = relationship(
        "PermissionModel",
        secondary="user_permissions",
        back_populates="users",
        lazy="joined",
    )
