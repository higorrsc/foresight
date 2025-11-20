from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm import relationship

from src.identity_access_management.infrastructure.models import user_roles
from src.shared_kernel.infrastructure.config import (
    SQLAlchemyBase,
    SQLAlchemyTenantMixin,
)


class RoleModel(SQLAlchemyBase, SQLAlchemyTenantMixin):
    """
    SQLAlchemy model for the Role entity.
    """

    __tablename__ = "roles"

    name = Column(
        String,
        index=True,
        nullable=False,
    )
    description = Column(
        String,
        nullable=True,
    )

    users_rel = relationship(
        "UserModel",
        secondary=user_roles,
        back_populates="roles_rel",
    )

    permissions_rel = relationship(
        "PermissionModel",
        secondary="role_permissions",
        back_populates="roles_rel",
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "tenant_id",
            name="uq_role_name_tenant",
        ),
    )
