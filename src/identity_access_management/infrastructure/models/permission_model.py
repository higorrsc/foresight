from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.core.infrastructure.config import SQLAlchemyBase
from src.identity_access_management.infrastructure.models import (
    role_permissions,
    user_permissions,
)


class PermissionModel(SQLAlchemyBase):
    """
    SQLAlchemy model for the Permission entity.
    """

    __tablename__ = "permissions"

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

    users_rel = relationship(
        "UserModel",
        secondary=user_permissions,
        back_populates="permissions_rel",
    )

    roles_rel = relationship(
        "RoleModel",
        secondary=role_permissions,
        back_populates="permissions_rel",
    )
