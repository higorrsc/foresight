from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from src.identity_access_management.infrastructure.repositories import (
    PermissionRepository,
    RoleRepository,
    UserRepository,
)
from src.shared_kernel.infrastructure.config import SessionLocal
from src.shared_kernel.infrastructure.repositories import (
    AreaRepository,
    OrganizationalUnitRepository,
)
from src.tenant_management.infrastructure.repositories import (
    PlanRepository,
    TenantRepository,
)


def get_db_session() -> Generator:  # pragma: no cover
    """
    Create a database session by request.
    """

    db = None

    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()


def get_area_repository(
    session: Session = Depends(get_db_session),
) -> AreaRepository:
    """
    Return an AreaRepository instance with database session.
    """

    return AreaRepository(session)


def get_user_repository(
    session: Session = Depends(get_db_session),
) -> UserRepository:
    """
    Return an UserRepository instance with database session.
    """

    return UserRepository(session)


def get_role_repository(
    session: Session = Depends(get_db_session),
) -> RoleRepository:
    """
    Return an RoleRepository instance with database session.
    """

    return RoleRepository(session)


def get_permission_repository(
    session: Session = Depends(get_db_session),
) -> PermissionRepository:
    """
    Return an PermissionRepository instance with database session.
    """

    return PermissionRepository(session)


def get_tenant_repository(
    session: Session = Depends(get_db_session),
) -> TenantRepository:
    """
    Return an TenantRepository instance with database session.
    """

    return TenantRepository(session)


def get_plan_repository(
    session: Session = Depends(get_db_session),
) -> PlanRepository:
    """
    Return an PlanRepository instance with database session.
    """

    return PlanRepository(session)


def get_organization_unit_repository(
    session: Session = Depends(get_db_session),
) -> OrganizationalUnitRepository:
    """
    Return an OrganizationalUnitRepository instance with database session.
    """

    return OrganizationalUnitRepository(session)
