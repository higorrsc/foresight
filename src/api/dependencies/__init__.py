from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.identity_access_management.domain.entities import User
from src.identity_access_management.domain.repositories import (
    IPermissionRepository,
    IRoleRepository,
    IUserRepository,
)
from src.planning.domain.repositories import (
    IExchangeRateRepository,
    IScenarioRepository,
)
from src.shared_kernel.domain.repositories import (
    IAreaRepository,
    IOrganizationalUnitRepository,
)
from src.tenant_management.domain.repositories import IPlanRepository, ITenantRepository

from .auth import get_auth_provider, get_current_user
from .authorization import PermissionChecker, RoleChecker
from .database import (
    get_area_repository,
    get_db_session,
    get_exchange_rate_repository,
    get_organizational_unit_repository,
    get_permission_repository,
    get_plan_repository,
    get_role_repository,
    get_scenario_repository,
    get_tenant_repository,
    get_user_repository,
)

# Shared Database/ORM dependencies
DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]

# IAM Dependencies
CurrentUserDep = Annotated[User, Depends(get_current_user)]
UserRepositoryDep = Annotated[IUserRepository, Depends(get_user_repository)]
RoleRepositoryDep = Annotated[IRoleRepository, Depends(get_role_repository)]
PermissionRepositoryDep = Annotated[
    IPermissionRepository, Depends(get_permission_repository)
]

# Tenant Dependencies
TenantRepositoryDep = Annotated[ITenantRepository, Depends(get_tenant_repository)]
PlanRepositoryDep = Annotated[IPlanRepository, Depends(get_plan_repository)]

# Shared Kernel Dependencies
AreaRepositoryDep = Annotated[IAreaRepository, Depends(get_area_repository)]
OrganizationalUnitRepositoryDep = Annotated[
    IOrganizationalUnitRepository, Depends(get_organizational_unit_repository)
]

# Planning Dependencies
ScenarioRepositoryDep = Annotated[IScenarioRepository, Depends(get_scenario_repository)]
ExchangeRateRepositoryDep = Annotated[
    IExchangeRateRepository, Depends(get_exchange_rate_repository)
]

__all__ = [
    "get_area_repository",
    "get_auth_provider",
    "get_current_user",
    "get_db_session",
    "get_exchange_rate_repository",
    "get_organizational_unit_repository",
    "get_permission_repository",
    "get_plan_repository",
    "get_role_repository",
    "get_scenario_repository",
    "get_tenant_repository",
    "get_user_repository",
    "PermissionChecker",
    "RoleChecker",
    "DbSessionDep",
    "CurrentUserDep",
    "UserRepositoryDep",
    "RoleRepositoryDep",
    "PermissionRepositoryDep",
    "TenantRepositoryDep",
    "PlanRepositoryDep",
    "AreaRepositoryDep",
    "OrganizationalUnitRepositoryDep",
    "ScenarioRepositoryDep",
    "ExchangeRateRepositoryDep",
]
