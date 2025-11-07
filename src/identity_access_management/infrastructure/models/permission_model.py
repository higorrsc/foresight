from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.identity_access_management.infrastructure.models import RoleModel, UserModel
from src.shared_kernel.infrastructure.config import Base, GUID_Type, SQLAlchemyBase

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

    users: Mapped[list["UserModel"]] = mapped_column(
        default_factory=list,
        init=False,
    )
    users_rel = relationship(
        "UserModel",
        secondary=user_permissions,
        back_populates="permissions_rel",
    )

    roles: Mapped[list["RoleModel"]] = mapped_column(
        default_factory=list,
        init=False,
    )
    roles_rel = relationship(
        "RoleModel",
        secondary=role_permissions,
        back_populates="permissions_rel",
    )
