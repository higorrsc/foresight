from sqlalchemy import Column, ForeignKey, Table

from src.shared_kernel.infrastructure.config import GUID_Type
from src.shared_kernel.infrastructure.config.base import Base

# Tabela de associação para User <-> Role
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

# Tabela de associação para User <-> Permission
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

# Tabela de associação para Role <-> Permission
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
