from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from src.identity_access_management.application.use_cases.user.exceptions import (
    UsernameAlreadyExistsError,
)
from src.identity_access_management.domain.entities import Role, User
from src.identity_access_management.domain.entities.user import hash_password
from src.identity_access_management.domain.repositories import (
    IPermissionRepository,
    IRoleRepository,
    IUserRepository,
)
from src.tenant_management.domain.entities.tenant import Tenant
from src.tenant_management.domain.repositories import IPlanRepository, ITenantRepository


@dataclass(frozen=True)
class OnboardingInputDTO:
    """
    Data Transfer Object for input data when creating a new user.
    """

    tenant_name: str
    username: str
    password: str
    first_name: Optional[str] = None
    email: Optional[str] = None
    plan_name: str = "Standard"


@dataclass(frozen=True)
class OnboardingOutputDTO:
    """
    Data Transfer Object for output data
    """

    user_id: UUID
    tenant_id: UUID


class OnboardingUseCase:
    """
    Use case to create a new user.
    """

    def __init__(
        self,
        plan_repository: IPlanRepository,
        tenant_repository: ITenantRepository,
        role_repository: IRoleRepository,
        user_repository: IUserRepository,
        permission_repository: IPermissionRepository,
    ):
        """ """

        self._plan_repo = plan_repository
        self._tenant_repo = tenant_repository
        self._role_repo = role_repository
        self._user_repo = user_repository
        self._perm_repo = permission_repository

    def execute(self, input_dto: OnboardingInputDTO) -> OnboardingOutputDTO:
        """
        Execute the use case to create a new user.
        """

        if self._user_repo.get_by_username_global(input_dto.username):
            raise UsernameAlreadyExistsError(
                f"Username '{input_dto.username}' already exists."
            )

        plan = self._plan_repo.get_by_name(input_dto.plan_name)
        if not plan:
            raise ValueError(f"Plan '{input_dto.plan_name}' not found.")

        new_tenant = Tenant(name=input_dto.tenant_name, plan_id=plan.id)
        self._tenant_repo.save(new_tenant)

        admin_role = Role(
            name="admin",
            description="Administrador do Tenant",
            tenant_id=new_tenant.id,
        )
        guest_role = Role(
            name="guest",
            description="Convidado do Tenant",
            tenant_id=new_tenant.id,
        )

        all_permissions = self._perm_repo.list_all()
        admin_role.permissions = {p.codename for p in all_permissions}

        self._role_repo.save(admin_role)
        self._role_repo.save(guest_role)

        new_user = User(
            tenant_id=new_tenant.id,
            username=input_dto.username,
            hashed_password=hash_password(input_dto.password),
            first_name=input_dto.first_name,
            email=input_dto.email,
            is_active=True,
            roles={admin_role.name},
        )

        if hasattr(new_user, "created_at"):
            new_user.created_at = datetime.now(timezone.utc)

        if hasattr(new_user, "updated_at"):
            new_user.updated_at = datetime.now(timezone.utc)

        self._user_repo.save(new_user)

        return OnboardingOutputDTO(user_id=new_user.id, tenant_id=new_tenant.id)
