from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.api.dependencies.auth import get_current_user
from src.api.dependencies.authorization import PermissionChecker
from src.api.dependencies.database import (
    get_permission_repository,
    get_plan_repository,
    get_role_repository,
    get_tenant_repository,
    get_user_repository,
)
from src.api.routers._shared.dto import PaginatedApiResponse
from src.identity_access_management.application.use_cases.permission import (
    InsufficientPermissionError,
)
from src.identity_access_management.application.use_cases.user.commands import (
    OnboardingInputDTO,
    OnboardingUseCase,
)
from src.identity_access_management.application.use_cases.user.exceptions import (
    UsernameAlreadyExistsError,
)
from src.identity_access_management.domain.entities import User
from src.identity_access_management.domain.repositories import (
    IPermissionRepository,
    IRoleRepository,
    IUserRepository,
)
from src.tenant_management.application.use_cases.tenant.commands import (
    UpdateTenantStatusInputDTO,
    UpdateTenantStatusUseCase,
)
from src.tenant_management.application.use_cases.tenant.exceptions import (
    TenantNotFoundError,
)
from src.tenant_management.application.use_cases.tenant.queries import (
    ListTenantsInputDTO,
    ListTenantsUseCase,
)
from src.tenant_management.domain.repositories import IPlanRepository, ITenantRepository
from src.tenant_management.domain.value_objects import TenantStatus


class SignupRequest(BaseModel):
    """
    Request model for API.
    """

    tenant_name: str = Field(..., min_length=3, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = None
    email: Optional[EmailStr] = None
    plan_name: str = "Standard"  # Valor padrão


class SignupResponse(BaseModel):
    """
    Response model for API.
    """

    tenant_id: UUID
    user_id: UUID
    message: str


class TenantResponse(BaseModel):
    """
    Response model for API.
    """

    id: UUID
    name: str
    status: TenantStatus
    plan_id: UUID

    model_config = ConfigDict(from_attributes=True)


class TenantStatusUpdateBody(BaseModel):
    """
    Request model for API.
    """

    status: TenantStatus


class PaginatedTenantResponse(PaginatedApiResponse[TenantResponse]):
    """
    Paginated response model for Tenants.
    """


require_tenant_read = PermissionChecker(["tenant:read"])
require_tenant_update = PermissionChecker(["tenant:update"])

router = APIRouter(prefix="/tenants", tags=["Tenant Management"])


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=SignupResponse,
)
def signup_endpoint(
    request: SignupRequest,
    plan_repo: IPlanRepository = Depends(get_plan_repository),
    tenant_repo: ITenantRepository = Depends(get_tenant_repository),
    role_repo: IRoleRepository = Depends(get_role_repository),
    user_repo: IUserRepository = Depends(get_user_repository),
    perm_repo: IPermissionRepository = Depends(get_permission_repository),
):
    """
    Register a new tenant and admin user.
    """

    try:
        use_case = OnboardingUseCase(
            plan_repository=plan_repo,
            tenant_repository=tenant_repo,
            role_repository=role_repo,
            user_repository=user_repo,
            permission_repository=perm_repo,
        )

        input_dto = OnboardingInputDTO(
            tenant_name=request.tenant_name,
            username=request.username,
            password=request.password,
            first_name=request.first_name,
            email=request.email,
            plan_name=request.plan_name,
        )

        result = use_case.execute(input_dto)

        return {
            "tenant_id": result.tenant_id,
            "user_id": result.user_id,
            "message": "Tenant e Administrador criados com sucesso.",
        }

    except UsernameAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedTenantResponse,
    dependencies=[Depends(require_tenant_read)],
)
def list_tenants_endpoint(
    repo: ITenantRepository = Depends(get_tenant_repository),
    actor: User = Depends(get_current_user),
):
    """
    List all tenants (Super Admin only).
    """
    try:
        use_case = ListTenantsUseCase(repo)
        input_dto = ListTenantsInputDTO(actor=actor)
        tenants = use_case.execute(input_dto)
        return tenants
    except InsufficientPermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        ) from e


@router.patch(
    "/{tenant_id}/status",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_tenant_update)],
)
def update_tenant_status_endpoint(
    tenant_id: UUID,
    body: TenantStatusUpdateBody,
    repo: ITenantRepository = Depends(get_tenant_repository),
    actor: User = Depends(get_current_user),
):
    """
    Update a tenant's status (e.g., suspend/activate) (Super Admin only).
    """
    try:
        use_case = UpdateTenantStatusUseCase(repo)
        input_dto = UpdateTenantStatusInputDTO(
            actor=actor,
            tenant_id_to_update=tenant_id,
            new_status=body.status,
        )
        use_case.execute(input_dto)
    except TenantNotFoundError as e:  # Tenant not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except InsufficientPermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        ) from e
