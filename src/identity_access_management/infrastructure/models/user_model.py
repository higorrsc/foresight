from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.core.infrastructure.config import SQLAlchemyBase
from src.core.infrastructure.config.mixins import (
    SQLAlchemySoftDeletableMixin,
    SQLAlchemyTenantMixin,
    SQLAlchemyUserAuditMixin,
)

from .association_tables import (
    user_permissions,
    user_roles,
)


class UserModel(
    SQLAlchemyBase,
    SQLAlchemyTenantMixin,
    SQLAlchemySoftDeletableMixin,
    SQLAlchemyUserAuditMixin,
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
    )

    permissions_rel = relationship(
        "PermissionModel",
        secondary=user_permissions,
        back_populates="users_rel",
    )
