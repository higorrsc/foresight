from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.identity_access_management.infrastructure.models import (
    user_permissions,
    user_roles,
)
from src.shared_kernel.infrastructure.config.sqlalchemy_base import SQLAlchemyBase
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

    roles_rel = relationship(
        "RoleModel",
        secondary=user_roles,
        back_populates="users_rel",
        lazy="joined",
    )

    permissions_rel = relationship(
        "PermissionModel",
        secondary=user_permissions,
        back_populates="users_rel",
        lazy="joined",
    )
