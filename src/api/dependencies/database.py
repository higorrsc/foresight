from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.infrastructure.config import SessionLocal
from src.identity_access_management.domain.repositories import (
    IPermissionRepository,
    IRoleRepository,
    IUserRepository,
)
from src.identity_access_management.infrastructure.repositories import (
    PermissionRepository,
    RoleRepository,
    UserRepository,
)
from src.planning.domain.repositories import (
    IExchangeRateRepository,
    IScenarioRepository,
)
from src.planning.infrastructure.repositories import (
    ExchangeRateRepository,
    ScenarioRepository,
)
from src.shared_kernel.domain.repositories import (
    IAreaRepository,
    IOrganizationalUnitRepository,
)
from src.shared_kernel.infrastructure.repositories import (
    AreaRepository,
    OrganizationalUnitRepository,
)
from src.tenant_management.domain.repositories import IPlanRepository, ITenantRepository
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
    session: Annotated[Session, Depends(get_db_session)],
) -> IAreaRepository:
    """
    Return an AreaRepository instance with database session.
    """

    return AreaRepository(session)


def get_user_repository(
    session: Annotated[Session, Depends(get_db_session)],
) -> IUserRepository:
    """
    Return an UserRepository instance with database session.
    """

    return UserRepository(session)


def get_role_repository(
    session: Annotated[Session, Depends(get_db_session)],
) -> IRoleRepository:
    """
    Return an RoleRepository instance with database session.
    """

    return RoleRepository(session)


def get_permission_repository(
    session: Annotated[Session, Depends(get_db_session)],
) -> IPermissionRepository:
    """
    Return an PermissionRepository instance with database session.
    """

    return PermissionRepository(session)


def get_tenant_repository(
    session: Annotated[Session, Depends(get_db_session)],
) -> ITenantRepository:
    """
    Return an TenantRepository instance with database session.
    """

    return TenantRepository(session)


def get_plan_repository(
    session: Annotated[Session, Depends(get_db_session)],
) -> IPlanRepository:
    """
    Return an PlanRepository instance with database session.
    """

    return PlanRepository(session)


def get_organizational_unit_repository(
    session: Annotated[Session, Depends(get_db_session)],
) -> IOrganizationalUnitRepository:
    """
    Return an OrganizationalUnitRepository instance with database session.
    """

    return OrganizationalUnitRepository(session)


def get_scenario_repository(
    session: Annotated[Session, Depends(get_db_session)],
) -> IScenarioRepository:
    """
    Return an ScenarioRepository instance with database session.
    """

    return ScenarioRepository(session)


def get_exchange_rate_repository(
    session: Annotated[Session, Depends(get_db_session)],
) -> IExchangeRateRepository:
    """
    Return an ExchangeRateRepository instance with database session.
    """

    return ExchangeRateRepository(session)
