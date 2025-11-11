from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

from src.api.dependencies.database import (
    get_permission_repository,
    get_plan_repository,
    get_role_repository,
    get_tenant_repository,
    get_user_repository,
)
from src.identity_access_management.application.use_cases.user import (
    UsernameAlreadyExistsError,
)
from src.identity_access_management.application.use_cases.user.commands import (
    OnboardingInputDTO,
    OnboardingUseCase,
)
from src.identity_access_management.infrastructure.repositories import (
    PermissionRepository,
    RoleRepository,
    UserRepository,
)
from src.tenant_management.infrastructure.repositories import (
    PlanRepository,
    TenantRepository,
)


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


router = APIRouter(prefix="/tenants", tags=["Tenant Management"])


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=SignupResponse,
)
def signup_endpoint(
    request: SignupRequest,
    plan_repo: PlanRepository = Depends(get_plan_repository),
    tenant_repo: TenantRepository = Depends(get_tenant_repository),
    role_repo: RoleRepository = Depends(get_role_repository),
    user_repo: UserRepository = Depends(get_user_repository),
    perm_repo: PermissionRepository = Depends(get_permission_repository),
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
