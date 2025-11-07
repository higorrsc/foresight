from typing import List

from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.identity_access_management.infrastructure.models.permission_model import (
    PermissionModel,
)
from src.identity_access_management.infrastructure.models.role_model import RoleModel
from src.shared_kernel.infrastructure.config import SQLAlchemyBase
from src.shared_kernel.infrastructure.models._shared.mixins import (
    SQLAlchemySoftDeletableMixin,
    SQLAlchemyTenantMixin,
)


class UserModel(
    SQLAlchemyBase,
    SQLAlchemyTenantMixin,
    SQLAlchemySoftDeletableMixin,
):
    """
    SQLAlchemy model for the User entity.
    """

    __tablename__ = "users"

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

    roles: Mapped[List["RoleModel"]] = mapped_column(
        default_factory=list,
        init=False,
    )
    roles_rel = relationship(
        "RoleModel",
        secondary="user_roles",
        back_populates="users_rel",
        lazy="joined",
    )

    permissions: Mapped[List["PermissionModel"]] = mapped_column(
        default_factory=list,
        init=False,
    )
    permissions_rel = relationship(
        "PermissionModel",
        secondary="user_permissions",
        back_populates="users_rel",
        lazy="joined",
    )
