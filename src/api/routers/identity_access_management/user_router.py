from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.api.dependencies import (
    PermissionChecker,
    get_current_user,
    get_permission_repository,
    get_role_repository,
    get_user_repository,
)
from src.api.routers._shared import PaginatedApiResponse
from src.core.application import PaginatedResponseDTO
from src.core.application.use_cases.commands import (
    DeleteRequestInputDTO,
    RestoreRequestInputDTO,
)
from src.core.application.use_cases.queries import (
    GetByIdRequestInputDTO,
    ListRequestInputDTO,
)
from src.identity_access_management.application.use_cases.user.commands import (
    ChangePasswordInputDTO,
    ChangePasswordUseCase,
    CreateUserInputDTO,
    CreateUserOutputDTO,
    CreateUserUseCase,
    DeleteUserUseCase,
    RestoreUserUseCase,
    SetUserPermissionsInputDTO,
    SetUserPermissionsUseCase,
    SetUserRolesInputDTO,
    SetUserRolesUseCase,
    UpdateUserProfileUseCase,
    UserProfileInputDTO,
)
from src.identity_access_management.application.use_cases.user.queries import (
    GetUserByIdUseCase,
    ListUserUseCase,
)
from src.identity_access_management.domain.entities import User
from src.identity_access_management.domain.exceptions import (
    InsufficientPermissionError,
    InvalidPasswordError,
    InvalidRoleError,
    PermissionNotFoundError,
    UsernameAlreadyExistsError,
    UserNotFoundError,
)
from src.identity_access_management.domain.repositories import (
    IPermissionRepository,
    IRoleRepository,
    IUserRepository,
)

require_user_change_password = PermissionChecker(["user:change_password"])
require_user_create = PermissionChecker(["user:create"])
require_user_delete = PermissionChecker(["user:delete"])
require_user_me = PermissionChecker(["user:me"])
require_user_read = PermissionChecker(["user:read"])
require_user_set_permissions = PermissionChecker(["user:set_permissions"])
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
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    roles: set[str] = set()
    permissions: set[str] = set()
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class PaginatedUserResponse(PaginatedApiResponse[UserSummaryResponse]):
    """
    Paginated response model for User.
    """


class UserCreateBody(BaseModel):
    """
    Request model for creating a user within a tenant.
    """

    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)
    roles: list[str] | None = Field(default_factory=list)  # type:ignore


class ChangePasswordBody(BaseModel):
    """
    Request model for changing password.
    """

    old_password: str
    new_password: str = Field(min_length=8)


class SetUserPermissionsBody(BaseModel):
    """
    Request model for setting user permissions.
    """

    permission_codes: list[str] = Field(default_factory=list)


class SetUserRolesBody(BaseModel):
    """
    Request model for setting user roles.
    """

    role_names: list[str] = Field(default_factory=list)


class UpdateUserProfileBody(BaseModel):
    """
    Request model for updating a user profile.
    """

    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    email: EmailStr | None = None


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
async def create_user_endpoint(
    request_body: UserCreateBody,
    user_repo: Annotated[IUserRepository, Depends(get_user_repository)],
    role_repo: Annotated[IRoleRepository, Depends(get_role_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> CreateUserOutputDTO:
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

        result = await use_case.execute(input_dto)
        return result

    except (UsernameAlreadyExistsError, InvalidRoleError) as e:
        status_code = (
            status.HTTP_409_CONFLICT
            if isinstance(e, UsernameAlreadyExistsError)
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(
            status_code=status_code,
            detail=str(e),
        ) from e
    except InsufficientPermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        ) from e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserDetailResponse,
    dependencies=[Depends(require_user_me)],
)
def get_current_user_me(
    actor: Annotated[User, Depends(get_current_user)],
) -> User:
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
async def list_users_endpoint(
    repo: Annotated[IUserRepository, Depends(get_user_repository)],
    actor: Annotated[User, Depends(get_current_user)],
    username: Annotated[
        str | None, Query(description="Filter by part of the username")
    ] = None,
    sort_by: Annotated[str | None, Query(description="Sort field")] = "username",
    sort_order: Annotated[
        str, Query(enum=["asc", "desc"], description="Sort order")
    ] = "asc",
    offset: Annotated[int, Query(ge=0, description="Offset for pagination")] = 0,
    limit: Annotated[
        int, Query(ge=1, le=100, description="Limit of records per page")
    ] = 10,
) -> PaginatedResponseDTO[User]:
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
    result = await use_case.execute(input_dto)

    return result


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserDetailResponse,
    dependencies=[Depends(require_user_read)],
)
async def get_user_by_id_endpoint(
    user_id: Annotated[UUID, Path(description="The user ID")],
    repo: Annotated[IUserRepository, Depends(get_user_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Get a specific user by their ID.
    """

    try:
        use_case = GetUserByIdUseCase(repo)
        input_dto = GetByIdRequestInputDTO(id=user_id, actor=actor)
        user = await use_case.execute(input_dto)
        return user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_user_delete)],
)
async def delete_user_endpoint(
    user_id: Annotated[UUID, Path(description="The user ID")],
    repo: Annotated[IUserRepository, Depends(get_user_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> None:
    """
    Delete an existing user (soft delete).
    """

    try:
        use_case = DeleteUserUseCase(repo)
        await use_case.execute(DeleteRequestInputDTO(id=user_id, actor=actor))
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
    except InsufficientPermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        ) from e


@router.patch(
    "/{user_id}/password",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_user_change_password)],
)
async def change_password_endpoint(
    user_id: Annotated[UUID, Path(description="The user ID")],
    request_body: ChangePasswordBody,
    repo: Annotated[IUserRepository, Depends(get_user_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> None:
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
        await use_case.execute(input_dto)
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
    except (ValueError, InsufficientPermissionError) as e:
        status_code = (
            status.HTTP_403_FORBIDDEN
            if isinstance(e, InsufficientPermissionError)
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(
            status_code=status_code,
            detail=str(e),
        ) from e


@router.patch(
    "/{user_id}/permissions",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_user_set_permissions)],
)
async def set_user_permissions_endpoint(
    user_id: Annotated[UUID, Path(description="The user ID")],
    request_body: SetUserPermissionsBody,
    user_repo: Annotated[IUserRepository, Depends(get_user_repository)],
    permission_repo: Annotated[
        IPermissionRepository,
        Depends(get_permission_repository),
    ],
    actor: Annotated[User, Depends(get_current_user)],
) -> None:
    """
    Set (overwrite) the permissions for a specific user. (Admin only)
    """

    try:
        use_case = SetUserPermissionsUseCase(
            user_repository=user_repo,
            permission_repository=permission_repo,
        )
        input_dto = SetUserPermissionsInputDTO(
            actor=actor,
            user_id_to_update=user_id,
            permissions_codes=request_body.permission_codes,
        )
        await use_case.execute(input_dto)
    except (UserNotFoundError, PermissionNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except (ValueError, InsufficientPermissionError) as e:
        status_code = (
            status.HTTP_403_FORBIDDEN
            if isinstance(e, InsufficientPermissionError)
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(
            status_code=status_code,
            detail=str(e),
        ) from e


@router.patch(
    "/{user_id}/profile",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_user_update_profile)],
)
async def update_user_profile_endpoint(
    user_id: Annotated[UUID, Path(description="The user ID")],
    request_body: UpdateUserProfileBody,
    repo: Annotated[IUserRepository, Depends(get_user_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> None:
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

    input_dto = UserProfileInputDTO(
        user_id_to_update=user_id,
        actor=actor,
        **update_data,
    )

    try:
        use_case = UpdateUserProfileUseCase(repo)
        await use_case.execute(input_dto)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except (ValueError, InsufficientPermissionError) as e:
        status_code = (
            status.HTTP_403_FORBIDDEN
            if isinstance(e, InsufficientPermissionError)
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(
            status_code=status_code,
            detail=str(e),
        ) from e


@router.patch(
    "/{user_id}/roles",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_user_set_roles)],
)
async def set_user_roles_endpoint(
    user_id: Annotated[UUID, Path(description="The user ID")],
    request_body: SetUserRolesBody,
    user_repo: Annotated[IUserRepository, Depends(get_user_repository)],
    role_repo: Annotated[IRoleRepository, Depends(get_role_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> None:
    """
    Set (overwrite) the roles for a specific user. (Admin only)
    """

    try:
        use_case = SetUserRolesUseCase(
            user_repository=user_repo,
            role_repository=role_repo,
        )
        input_dto = SetUserRolesInputDTO(
            actor=actor,
            user_id_to_update=user_id,
            role_names=request_body.role_names,
        )
        await use_case.execute(input_dto)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except (ValueError, InsufficientPermissionError) as e:
        status_code = (
            status.HTTP_403_FORBIDDEN
            if isinstance(e, InsufficientPermissionError)
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(
            status_code=status_code,
            detail=str(e),
        ) from e


@router.patch(
    "/{user_id}/restore",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_user_delete)],
)
async def restore_user_endpoint(
    user_id: Annotated[UUID, Path(description="The user ID")],
    repo: Annotated[IUserRepository, Depends(get_user_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> None:
    """
    Restore a soft-deleted user.
    """

    try:
        use_case = RestoreUserUseCase(repo)
        await use_case.execute(RestoreRequestInputDTO(id=user_id, actor=actor))
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
