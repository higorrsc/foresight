from typing import Protocol, TypeGuard
from uuid import UUID


class SoftDeletable(Protocol):
    """Protocol for soft deletable entities."""

    is_active: bool


class UserAuditable(Protocol):
    """Protocol for user auditable entities."""

    created_by: UUID
    updated_by: UUID


class HasTenant(Protocol):
    """Protocol for tenant entities."""

    tenant_id: UUID


def has_tenant(obj: object) -> TypeGuard[HasTenant]:
    """
    Check if an object is a tenant entity.

    Args:
        obj (object): The object to check.

    Returns:
        bool: True if the object is a tenant entity, False otherwise.
    """

    return hasattr(obj, "tenant_id")


def is_soft_deletable(obj: object) -> TypeGuard[SoftDeletable]:
    """
    Check if an object is a soft deletable entity.

    Args:
        obj (object): The object to check.

    Returns:
        bool: True if the object is a soft deletable entity, False otherwise.
    """

    return hasattr(obj, "is_active")


def is_user_auditable(obj: object) -> TypeGuard[UserAuditable]:
    """
    Check if an object is a user auditable entity.

    Args:
        obj (object): The object to check.

    Returns:
        bool: True if the object is a user auditable entity, False otherwise.
    """

    return hasattr(obj, "created_by") and hasattr(obj, "updated_by")
