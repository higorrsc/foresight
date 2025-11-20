from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict, Field

from src.api.dependencies.auth import get_current_user
from src.api.dependencies.authorization import PermissionChecker
from src.api.dependencies.database import get_role_repository
from src.api.routers._shared import PaginatedApiResponse
from src.identity_access_management.application.use_cases.role import (
    InvalidRoleError,
    RoleAlreadyExistsError,
    RoleNotFoundError,
)
from src.identity_access_management.application.use_cases.role.commands import (
    CreateRoleInputDTO,
    CreateRoleUseCase,
    DeleteRoleUseCase,
    UpdateRoleInputDTO,
    UpdateRoleUseCase,
)
from src.identity_access_management.application.use_cases.role.queries import (
    GetRoleByIdUseCase,
    ListRoleUseCase,
)
from src.identity_access_management.domain.entities import User
from src.identity_access_management.infrastructure.repositories import RoleRepository
from src.shared_kernel.application._shared.use_cases.commands import (
    DeleteRequestInputDTO,
)
from src.shared_kernel.application._shared.use_cases.queries import (
    GetByIdRequestInputDTO,
    ListRequestInputDTO,
)

# --- Permissions ---
require_role_create_or_update = PermissionChecker(["role:create", "role:update"])
require_role_delete = PermissionChecker(["role:delete"])
require_role_read = PermissionChecker(["role:read"])


# --- Response Models ---
class RoleResponse(BaseModel):
    """
    Response model for Role API.
    """

    id: UUID
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedRoleResponse(PaginatedApiResponse[RoleResponse]):
    """
    Paginated response model for Role.
    """


# --- Request Body Models ---
class RoleCreateBody(BaseModel):
    """
    Request model for creating or updating a role.
    """

    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=255)


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
def create_role_endpoint(
    request_body: RoleCreateBody,
    repo: RoleRepository = Depends(get_role_repository),
    actor: User = Depends(get_current_user),
):
    """
    Create a new role in the current tenant.
    """
    try:
        use_case = CreateRoleUseCase(repo)

        # Manual DTO construction
        input_dto = CreateRoleInputDTO(
            actor=actor,
            name=request_body.name,
            description=request_body.description,
        )

        result = use_case.execute(input_dto)
        return {"id": result.id}
    except (InvalidRoleError, RoleAlreadyExistsError) as e:
        status_code = (
            status.HTTP_409_CONFLICT
            if isinstance(e, RoleAlreadyExistsError)
            else status.HTTP_422_UNPROCESSABLE_CONTENT
        )
        raise HTTPException(status_code=status_code, detail=str(e)) from e


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedRoleResponse,
    dependencies=[Depends(require_role_read)],
)
def list_roles_endpoint(
    repo: RoleRepository = Depends(get_role_repository),
    actor: User = Depends(get_current_user),
    name: Optional[str] = Query(None, description="Filter by part of the name"),
    sort_by: Optional[str] = Query("name", description="Sort field"),
    sort_order: str = Query("asc", enum=["asc", "desc"], description="Sort order"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Limit of records per page"),
):
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
    result = use_case.execute(input_dto)
    return result


@router.get(
    "/{role_id}",
    status_code=status.HTTP_200_OK,
    response_model=RoleResponse,
    dependencies=[Depends(require_role_read)],
)
def get_role_by_id_endpoint(
    role_id: UUID,
    repo: RoleRepository = Depends(get_role_repository),
    actor: User = Depends(get_current_user),
):
    """
    Get a role by its ID.
    """
    try:
        use_case = GetRoleByIdUseCase(repo)
        input_dto = GetByIdRequestInputDTO(id=role_id, actor=actor)
        role = use_case.execute(input_dto)
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
def update_role_endpoint(
    role_id: UUID,
    request_body: RoleCreateBody,
    repo: RoleRepository = Depends(get_role_repository),
    actor: User = Depends(get_current_user),
):
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

        output_dto = use_case.execute(input_dto)
        return {"id": output_dto.id, "name": output_dto.name}
    except (RoleNotFoundError, RoleAlreadyExistsError, InvalidRoleError) as e:
        if isinstance(e, RoleNotFoundError):
            status_code = status.HTTP_404_NOT_FOUND
        elif isinstance(e, RoleAlreadyExistsError):
            status_code = status.HTTP_409_CONFLICT
        else:
            status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
        raise HTTPException(status_code=status_code, detail=str(e)) from e


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role_delete)],
)
def delete_role_endpoint(
    role_id: UUID,
    repo: RoleRepository = Depends(get_role_repository),
    actor: User = Depends(get_current_user),
):
    """
    Delete an existing role.
    """
    try:
        use_case = DeleteRoleUseCase(repo)
        use_case.execute(DeleteRequestInputDTO(id=role_id, actor=actor))
    except RoleNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
