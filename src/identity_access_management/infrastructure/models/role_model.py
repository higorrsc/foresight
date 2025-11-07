from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.identity_access_management.infrastructure.models import (
    PermissionModel,
    UserModel,
)
from src.shared_kernel.infrastructure.config import Base, GUID_Type, SQLAlchemyBase
from src.shared_kernel.infrastructure.models._shared.mixins import SQLAlchemyTenantMixin

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


class RoleModel(SQLAlchemyBase, SQLAlchemyTenantMixin):
    """
    SQLAlchemy model for the Role entity.
    """

    __tablename__ = "roles"

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

    users: Mapped[list["UserModel"]] = mapped_column(
        default_factory=list,
        init=False,
    )
    users_rel = relationship(
        "UserModel",
        secondary=user_roles,
        back_populates="roles_rel",
    )

    permissions: Mapped[list["PermissionModel"]] = mapped_column(
        default_factory=list,
        init=False,
    )
    permissions_rel = relationship(
        "PermissionModel",
        secondary="role_permissions",
        back_populates="roles_rel",
    )
