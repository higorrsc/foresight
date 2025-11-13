from datetime import datetime
from typing import List, Optional, Set
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.api.dependencies.auth import get_current_user
from src.api.dependencies.authorization import RoleChecker
from src.api.dependencies.database import (
    get_permission_repository,
    get_plan_repository,
    get_role_repository,
    get_tenant_repository,
    get_user_repository,
)
from src.api.routers._shared import PaginationMetaResponse
from src.identity_access_management.application.use_cases.role import InvalidRoleError
from src.identity_access_management.application.use_cases.user import (
    InvalidPasswordError,
    InvalidUserError,
    UsernameAlreadyExistsError,
    UserNotFoundError,
)
from src.identity_access_management.application.use_cases.user.commands import (
    ChangePasswordInputDTO,
    ChangePasswordUseCase,
    DeleteUserUseCase,
    OnboardingInputDTO,
    OnboardingUseCase,
    RestoreUserUseCase,
    UpdateUserProfileUseCase,
    UserProfileRequestDTO,
)
from src.identity_access_management.application.use_cases.user.queries import (
    GetUserByIdUseCase,
    ListUserUseCase,
)
from src.identity_access_management.domain.entities.user import User
from src.identity_access_management.infrastructure.repositories import (
    PermissionRepository,
    RoleRepository,
    UserRepository,
)
from src.shared_kernel.application._shared.use_cases.commands import (
    DeleteRequestInputDTO,
    RestoreRequestInputDTO,
)
from src.shared_kernel.application._shared.use_cases.queries import (
    GetByIdRequestInputDTO,
    ListRequestInputDTO,
)
from src.tenant_management.infrastructure.repositories import (
    PlanRepository,
    TenantRepository,
)

allow_admin_only = RoleChecker(["admin"])


class UserSummaryResponse(BaseModel):
    """
    Class that represents a user summary response.
    """

    id: UUID
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserDetailResponse(BaseModel):
    """
    Class that represents a user detailed response.
    """

    id: UUID
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    roles: Set[str] = set()

    model_config = ConfigDict(from_attributes=True)


class PaginatedUserResponse(BaseModel):
    """
    Response model for API.
    """

    data: List[UserSummaryResponse]
    meta: PaginationMetaResponse

    model_config = ConfigDict(from_attributes=True)


class ChangePasswordBody(BaseModel):
    """
    Request model for change password.
    """

    old_password: str
    new_password: str = Field(..., min_length=8)


class UpdateUserProfileBody(BaseModel):
    """
    Request model for update profile.
    """

    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


public_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

protected_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[
        Depends(get_current_user),
    ],
)


@public_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSummaryResponse,
)
def create_user_endpoint(
    request: OnboardingInputDTO,
    plan_repo: PlanRepository = Depends(get_plan_repository),
    tenant_repo: TenantRepository = Depends(get_tenant_repository),
    role_repo: RoleRepository = Depends(get_role_repository),
    permission_repo: PermissionRepository = Depends(get_permission_repository),
    user_repo: UserRepository = Depends(get_user_repository),
):
    """
    Create a new user.
    """

    try:
        use_case = OnboardingUseCase(
            plan_repository=plan_repo,
            tenant_repository=tenant_repo,
            role_repository=role_repo,
            user_repository=user_repo,
            permission_repository=permission_repo,
        )
        result = use_case.execute(request)
        return result
    except UsernameAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
    except InvalidRoleError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@protected_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedUserResponse,
)
def list_users_endpoint(
    repo: UserRepository = Depends(get_user_repository),
    actor: User = Depends(get_current_user),
    username: str = Query(None, description="Filtrar por parte do username"),
    sort_by: str = Query("username", description="Campo para ordenação"),
    sort_order: str = Query("asc", enum=["asc", "desc"]),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    """
    List users with filters, order and pagination.
    """

    filters = {"username": username} if username else {}
    input_dto = ListRequestInputDTO(
        actor=actor,
        filters=filters,
        sort_by=sort_by,
        sort_order=sort_order,
        offset=offset,
        limit=limit,
    )
    use_case = ListUserUseCase(repository=repo)
    result = use_case.execute(input_dto)

    return result


@protected_router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserDetailResponse,
)
def get_user_by_id_endpoint(
    user_id: UUID,
    repo: UserRepository = Depends(get_user_repository),
    actor: User = Depends(get_current_user),
):
    """
    Getting an user by its ID.
    """

    try:
        use_case = GetUserByIdUseCase(repo)
        input_dto = GetByIdRequestInputDTO(actor=actor, id=user_id)
        user = use_case.execute(input_dto)
        return user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@protected_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(allow_admin_only)],
)
def delete_user_endpoint(
    user_id: UUID,
    repo: UserRepository = Depends(get_user_repository),
    actor: User = Depends(get_current_user),
):
    """
    Delete an existing user.
    """

    try:
        use_case = DeleteUserUseCase(repository=repo)
        use_case.execute(DeleteRequestInputDTO(actor=actor, id=user_id))
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@protected_router.patch(
    "/{user_id}/password",
    status_code=status.HTTP_204_NO_CONTENT,
)
def change_password_endpoint(
    user_id: UUID,
    request_body: ChangePasswordBody,
    repo: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user),
):
    """
    Change the password of an existing user.
    """

    if ("admin" not in current_user.roles) and (current_user.id != user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update another user's password",
        )

    try:
        use_case = ChangePasswordUseCase(repository=repo)
        input_dto = ChangePasswordInputDTO(
            actor=current_user,
            user_id_to_change=user_id,
            old_password=request_body.old_password,
            new_password=request_body.new_password,
        )
        use_case.execute(input_dto)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except InvalidPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@protected_router.patch(
    "/{user_id}/profile",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_profile_endpoint(
    user_id: UUID,
    request_body: UpdateUserProfileBody,
    repo: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user),
):
    """
    Update the profile of an existing user.
    """

    if ("admin" not in current_user.roles) and (current_user.id != user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update another user's profile",
        )

    updated_data = request_body.model_dump(exclude_unset=True)
    input_dto = UserProfileRequestDTO(
        actor=current_user,
        user_id_to_update=user_id,
        **updated_data,
    )

    try:
        use_case = UpdateUserProfileUseCase(repository=repo)
        use_case.execute(input_dto=input_dto)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except InvalidUserError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@protected_router.patch(
    "/{user_id}/restore",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(allow_admin_only)],
)
def restore_user_endpoint(
    user_id: UUID,
    repo: UserRepository = Depends(get_user_repository),
    actor: User = Depends(get_current_user),
):
    """
    Restore an existing user.
    """

    try:
        use_case = RestoreUserUseCase(repository=repo)
        use_case.execute(RestoreRequestInputDTO(actor=actor, id=user_id))
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
