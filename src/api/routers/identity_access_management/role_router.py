from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, ConfigDict, Field

from src.api.dependencies import (
    PermissionChecker,
    get_current_user,
    get_permission_repository,
    get_role_repository,
    get_user_repository,
)
from src.api.routers._shared import PaginatedApiResponse
from src.core.application import PaginatedResponseDTO
from src.core.application.use_cases.commands import DeleteRequestInputDTO
from src.core.application.use_cases.commands.generic_restore import (
    RestoreRequestInputDTO,
)
from src.core.application.use_cases.queries import (
    GetByIdRequestInputDTO,
    ListRequestInputDTO,
)
from src.identity_access_management.application.use_cases.role.commands import (
    CreateRoleInputDTO,
    CreateRoleUseCase,
    DeleteRoleUseCase,
    RestoreRoleUseCase,
    SetRolePermissionsInputDTO,
    SetRolePermissionsUseCase,
    UpdateRoleInputDTO,
    UpdateRoleUseCase,
)
from src.identity_access_management.application.use_cases.role.queries import (
    GetRoleByIdUseCase,
    ListRoleUseCase,
)
from src.identity_access_management.domain.entities import Role, User
from src.identity_access_management.domain.exceptions import (
    InsufficientPermissionError,
    InvalidRoleError,
    PermissionNotFoundError,
    RoleAlreadyExistsError,
    RoleDeletionIntegrityError,
    RoleNotFoundError,
)
from src.identity_access_management.domain.repositories import (
    IPermissionRepository,
    IRoleRepository,
    IUserRepository,
)

# --- Permissions ---
require_role_create_or_update = PermissionChecker(["role:create", "role:update"])
require_role_delete = PermissionChecker(["role:delete"])
require_role_read = PermissionChecker(["role:read"])
require_role_set_permissions = PermissionChecker(["role:set_permissions"])


# --- Response Models ---
class RoleSummaryResponse(BaseModel):
    """
    Summary response model for Role (used in lists).
    """

    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class RoleDetailResponse(BaseModel):
    """
    Response model for Role API.
    """

    id: UUID
    name: str
    description: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    permissions: set[str] = set()

    model_config = ConfigDict(from_attributes=True)


class PaginatedRoleResponse(PaginatedApiResponse[RoleSummaryResponse]):
    """
    Paginated response model for Role.
    """


# --- Request Body Models ---
class RoleCreateBody(BaseModel):
    """
    Request model for creating or updating a role.
    """

    name: str = Field(min_length=3, max_length=100)
    description: str | None = Field(None, max_length=255)
    permissions: set[str] = set()


class SetRolePermissionsBody(BaseModel):
    """
    Request model for setting role permissions.
    """

    permission_codes: list[str] = Field(default_factory=list)


# --- Router ---
router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    dependencies=[Depends(get_current_user)],
)


# --- Endpoints ---


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role_create_or_update)],
)
async def create_role_endpoint(
    request_body: RoleCreateBody,
    role_repo: Annotated[IRoleRepository, Depends(get_role_repository)],
    permission_repo: Annotated[
        IPermissionRepository, Depends(get_permission_repository)
    ],
    actor: Annotated[User, Depends(get_current_user)],
) -> dict[str, UUID]:
    """
    Create a new role in the current tenant.
    """
    try:
        use_case = CreateRoleUseCase(
            role_repo,
            permission_repo,
        )

        # Manual DTO construction
        input_dto = CreateRoleInputDTO(
            actor=actor,
            name=request_body.name,
            description=request_body.description,
            permissions=request_body.permissions,  # type: ignore
        )

        result = await use_case.execute(input_dto)
        return {"id": result.id}
    except (InvalidRoleError, RoleAlreadyExistsError) as e:
        status_code = (
            status.HTTP_409_CONFLICT
            if isinstance(e, RoleAlreadyExistsError)
            else status.HTTP_422_UNPROCESSABLE_CONTENT
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
    except (ValueError, PermissionNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedRoleResponse,
    dependencies=[Depends(require_role_read)],
)
async def list_roles_endpoint(
    repo: Annotated[IRoleRepository, Depends(get_role_repository)],
    actor: Annotated[User, Depends(get_current_user)],
    name: Annotated[str | None, Query(description="Filter by part of the name")] = None,
    sort_by: Annotated[str | None, Query(description="Sort field")] = "name",
    sort_order: Annotated[
        str, Query(enum=["asc", "desc"], description="Sort order")
    ] = "asc",
    offset: Annotated[int, Query(ge=0, description="Offset for pagination")] = 0,
    limit: Annotated[
        int, Query(ge=1, le=100, description="Limit of records per page")
    ] = 10,
) -> PaginatedResponseDTO[Role]:
    """
    List roles with filters, order and pagination.
    """
    filters = {}
    if name:
        filters["name"] = name

    input_dto = ListRequestInputDTO(
        actor=actor,
        filters=filters,
        sort_by=sort_by,
        sort_order=sort_order,
        offset=offset,
        limit=limit,
    )
    use_case = ListRoleUseCase(repo)

    # Use Case returns PaginatedResponseDTO, compatible with PaginatedRoleResponse
    result = await use_case.execute(input_dto)
    return result


@router.get(
    "/{role_id}",
    status_code=status.HTTP_200_OK,
    response_model=RoleDetailResponse,
    dependencies=[Depends(require_role_read)],
)
async def get_role_by_id_endpoint(
    role_id: Annotated[UUID, Path(description="The role ID")],
    repo: Annotated[IRoleRepository, Depends(get_role_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> Role:
    """
    Get a role by its ID.
    """
    try:
        use_case = GetRoleByIdUseCase(repo)
        input_dto = GetByIdRequestInputDTO(id=role_id, actor=actor)
        role = await use_case.execute(input_dto)
        return role
    except RoleNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.put(
    "/{role_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role_create_or_update)],
)
async def update_role_endpoint(
    role_id: Annotated[UUID, Path(description="The role ID")],
    request_body: RoleCreateBody,
    repo: Annotated[IRoleRepository, Depends(get_role_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> dict[str, UUID | str]:
    """
    Update an existing role.
    """
    try:
        use_case = UpdateRoleUseCase(repo)

        # Manual DTO construction
        input_dto = UpdateRoleInputDTO(
            id=role_id,
            actor=actor,
            name=request_body.name,
            description=request_body.description,
        )

        output_dto = await use_case.execute(input_dto)
        return {"id": output_dto.id, "name": output_dto.name}
    except (RoleNotFoundError, RoleAlreadyExistsError, InvalidRoleError) as e:
        if isinstance(e, RoleNotFoundError):
            status_code = status.HTTP_404_NOT_FOUND
        elif isinstance(e, RoleAlreadyExistsError):
            status_code = status.HTTP_409_CONFLICT
        else:
            status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
        raise HTTPException(
            status_code=status_code,
            detail=str(e),
        ) from e


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role_delete)],
)
async def delete_role_endpoint(
    role_id: Annotated[UUID, Path(description="The role ID")],
    role_repo: Annotated[IRoleRepository, Depends(get_role_repository)],
    user_repo: Annotated[IUserRepository, Depends(get_user_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> None:
    """
    Delete an existing role.
    """
    try:
        use_case = DeleteRoleUseCase(
            role_repo,
            user_repo,
        )
        await use_case.execute(DeleteRequestInputDTO(id=role_id, actor=actor))
    except (RoleNotFoundError, RoleDeletionIntegrityError) as e:
        status_code = (
            status.HTTP_404_NOT_FOUND
            if isinstance(e, RoleNotFoundError)
            else status.HTTP_400_BAD_REQUEST
        )
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
    "/{role_id}/permissions",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role_set_permissions)],
)
async def set_role_permissions_endpoint(
    role_id: Annotated[UUID, Path(description="The role ID")],
    request_body: SetRolePermissionsBody,
    role_repo: Annotated[IRoleRepository, Depends(get_role_repository)],
    permission_repo: Annotated[
        IPermissionRepository, Depends(get_permission_repository)
    ],
    actor: Annotated[User, Depends(get_current_user)],
) -> None:
    """
    Set (overwrite) the permissions for a specific role. (Admin only)
    """

    try:
        use_case = SetRolePermissionsUseCase(
            role_repository=role_repo,
            permission_repository=permission_repo,
        )
        input_dto = SetRolePermissionsInputDTO(
            actor=actor,
            role_id_to_update=role_id,
            permissions_codes=request_body.permission_codes,
        )
        await use_case.execute(input_dto)
    except (RoleNotFoundError, PermissionNotFoundError) as e:
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
    "/{role_id}/restore",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role_delete)],
)
async def restore_user_endpoint(
    role_id: Annotated[UUID, Path(description="The role ID")],
    repo: Annotated[IRoleRepository, Depends(get_role_repository)],
    actor: Annotated[User, Depends(get_current_user)],
) -> None:
    """
    Restore a soft-deleted user.
    """

    try:
        use_case = RestoreRoleUseCase(repo)
        await use_case.execute(RestoreRequestInputDTO(id=role_id, actor=actor))
    except RoleNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
