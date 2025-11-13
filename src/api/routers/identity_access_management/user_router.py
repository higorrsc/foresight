from datetime import datetime
from typing import List, Optional, Set
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.api.dependencies.auth import get_current_user
from src.api.dependencies.authorization import PermissionChecker
from src.api.dependencies.database import get_role_repository, get_user_repository
from src.api.routers._shared import PaginatedApiResponse
from src.identity_access_management.application.use_cases.role import InvalidRoleError
from src.identity_access_management.application.use_cases.user import (
    InvalidPasswordError,
    UsernameAlreadyExistsError,
    UserNotFoundError,
)
from src.identity_access_management.application.use_cases.user.commands import (
    ChangePasswordInputDTO,
    ChangePasswordUseCase,
    CreateUserInputDTO,
    CreateUserUseCase,
    DeleteUserUseCase,
    SetUserRolesRequestDTO,
    SetUserRolesUseCase,
    UpdateUserProfileUseCase,
    UserProfileRequestDTO,
)
from src.identity_access_management.application.use_cases.user.exceptions import (
    InsufficientPermissionError,
)
from src.identity_access_management.application.use_cases.user.queries import (
    GetUserByIdUseCase,
    ListUserUseCase,
)
from src.identity_access_management.domain.entities.user import User
from src.identity_access_management.infrastructure.repositories import (
    RoleRepository,
    UserRepository,
)
from src.shared_kernel.application._shared.use_cases.commands import (
    DeleteRequestInputDTO,
)
from src.shared_kernel.application._shared.use_cases.queries import (
    GetByIdRequestInputDTO,
    ListRequestInputDTO,
)

require_user_change_password = PermissionChecker(["user:change_password"])
require_user_create = PermissionChecker(["user:create"])
require_user_delete = PermissionChecker(["user:delete"])
require_user_me = PermissionChecker(["user:me"])
require_user_read = PermissionChecker(["user:read"])
require_user_set_roles = PermissionChecker(["user:set_roles"])
require_user_update = PermissionChecker(["user:update"])
require_user_update_profile = PermissionChecker(["user:update_profile"])


class UserSummaryResponse(BaseModel):
    """
    Summary response model for User (used in lists).
    """

    id: UUID
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserDetailResponse(BaseModel):
    """
    Detailed response model for User.
    """

    id: UUID
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    roles: Set[str] = set()
    permissions: Set[str] = set()
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PaginatedUserResponse(PaginatedApiResponse[UserSummaryResponse]):
    """
    Paginated response model for User.
    """


class UserCreateBody(BaseModel):
    """
    Request model for creating a user within a tenant.
    """

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    roles: Optional[List[str]] = Field(default_factory=list)


class ChangePasswordBody(BaseModel):
    """
    Request model for changing password.
    """

    old_password: str
    new_password: str = Field(..., min_length=8)


class SetUserRolesBody(BaseModel):
    """
    Request model for setting user roles.
    """

    role_names: List[str] = Field(default_factory=list)


class UpdateUserProfileBody(BaseModel):
    """
    Request model for updating a user profile.
    """

    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSummaryResponse,
    dependencies=[Depends(require_user_create)],
)
def create_user_endpoint(
    request_body: UserCreateBody,
    user_repo: UserRepository = Depends(get_user_repository),
    role_repo: RoleRepository = Depends(get_role_repository),
    actor: User = Depends(get_current_user),
):
    """
    Create a new user in the current tenant (Admin only).
    """

    try:
        use_case = CreateUserUseCase(
            user_repository=user_repo,
            role_repository=role_repo,
        )

        input_dto = CreateUserInputDTO(
            actor=actor,
            username=request_body.username,
            password=request_body.password,
            roles=request_body.roles,  # type: ignore
        )

        result = use_case.execute(input_dto)
        return result

    except (UsernameAlreadyExistsError, InvalidRoleError) as e:
        status_code = (
            status.HTTP_409_CONFLICT
            if isinstance(e, UsernameAlreadyExistsError)
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=str(e)) from e
    except InsufficientPermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserDetailResponse,
    dependencies=[Depends(require_user_me)],
)
def get_current_user_me(actor: User = Depends(get_current_user)):
    """
    Get the details of the currently authenticated user.
    """

    return actor


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedUserResponse,
    dependencies=[Depends(require_user_read)],
)
def list_users_endpoint(
    repo: UserRepository = Depends(get_user_repository),
    actor: User = Depends(get_current_user),
    username: Optional[str] = Query(None, description="Filter by part of the username"),
    sort_by: Optional[str] = Query("username", description="Sort field"),
    sort_order: str = Query("asc", enum=["asc", "desc"], description="Sort order"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Limit of records per page"),
):
    """
    List users with filters, order and pagination.
    """

    filters = {}
    if username:
        filters["username"] = username

    input_dto = ListRequestInputDTO(
        actor=actor,
        filters=filters,
        sort_by=sort_by,
        sort_order=sort_order,
        offset=offset,
        limit=limit,
    )
    use_case = ListUserUseCase(repo)
    result = use_case.execute(input_dto)

    return result


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserDetailResponse,
    dependencies=[Depends(require_user_read)],
)
def get_user_by_id_endpoint(
    user_id: UUID,
    repo: UserRepository = Depends(get_user_repository),
    actor: User = Depends(get_current_user),
):
    """
    Get a specific user by their ID.
    """

    try:
        use_case = GetUserByIdUseCase(repo)
        input_dto = GetByIdRequestInputDTO(id=user_id, actor=actor)
        user = use_case.execute(input_dto)
        return user
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_user_delete)],
)
def delete_user_endpoint(
    user_id: UUID,
    repo: UserRepository = Depends(get_user_repository),
    actor: User = Depends(get_current_user),
):
    """
    Delete an existing user (soft delete).
    """

    try:
        use_case = DeleteUserUseCase(repo)
        use_case.execute(DeleteRequestInputDTO(id=user_id, actor=actor))
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    except InsufficientPermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e)) from e


@router.patch(
    "/{user_id}/password",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_user_change_password)],
)
def change_password_endpoint(
    user_id: UUID,
    request_body: ChangePasswordBody,
    repo: UserRepository = Depends(get_user_repository),
    actor: User = Depends(get_current_user),
):
    """
    Change a user's password.
    Users can change their own password. Admins can change anyone's.
    """

    try:
        use_case = ChangePasswordUseCase(repo)
        input_dto = ChangePasswordInputDTO(
            actor=actor,
            user_id_to_change=user_id,
            old_password=request_body.old_password,
            new_password=request_body.new_password,
        )
        use_case.execute(input_dto)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except InvalidPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    except (ValueError, InsufficientPermissionError) as e:
        status_code = (
            status.HTTP_403_FORBIDDEN
            if isinstance(e, InsufficientPermissionError)
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=str(e)) from e


@router.patch(
    "/{user_id}/profile",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_user_update_profile)],
)
def update_user_profile_endpoint(
    user_id: UUID,
    request_body: UpdateUserProfileBody,
    repo: UserRepository = Depends(get_user_repository),
    actor: User = Depends(get_current_user),
):
    """
    Partially update a user's profile.
    Admins can update anyone. Users can only update their own profile.
    """

    update_data = request_body.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields provided for update.",
        )

    input_dto = UserProfileRequestDTO(
        user_id_to_update=user_id,
        actor=actor,
        **update_data,
    )

    try:
        use_case = UpdateUserProfileUseCase(repo)
        use_case.execute(input_dto)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except (ValueError, InsufficientPermissionError) as e:
        status_code = (
            status.HTTP_403_FORBIDDEN
            if isinstance(e, InsufficientPermissionError)
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=str(e)) from e


@router.patch(
    "/{user_id}/roles",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_user_set_roles)],
)
def set_user_roles_endpoint(
    user_id: UUID,
    request_body: SetUserRolesBody,
    user_repo: UserRepository = Depends(get_user_repository),
    role_repo: RoleRepository = Depends(get_role_repository),
    actor: User = Depends(get_current_user),
):
    """
    Set (overwrite) the roles for a specific user. (Admin only)
    """

    try:
        use_case = SetUserRolesUseCase(
            user_repository=user_repo,
            role_repository=role_repo,
        )
        input_dto = SetUserRolesRequestDTO(
            actor=actor,
            user_id_to_update=user_id,
            role_names=request_body.role_names,
        )
        use_case.execute(input_dto)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except (ValueError, InsufficientPermissionError) as e:
        # InsufficientPermissionError (business rule) -> 403
        # ValueError (role not found) -> 400
        status_code = (
            status.HTTP_403_FORBIDDEN
            if isinstance(e, InsufficientPermissionError)
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=str(e)) from e
