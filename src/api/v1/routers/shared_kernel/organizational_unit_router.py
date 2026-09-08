from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, ConfigDict, Field

from src.api.dependencies import (
    CurrentUserDep,
    OrganizationalUnitRepositoryDep,
    PermissionChecker,
    get_current_user,
)
from src.api.v1.routers._shared import PaginatedApiResponse
from src.core.application import PaginatedResponseDTO
from src.core.application.use_cases.commands.generic_delete import DeleteRequestInputDTO
from src.core.application.use_cases.commands.generic_restore import (
    RestoreRequestInputDTO,
)
from src.core.application.use_cases.queries import (
    GetByIdRequestInputDTO,
    ListRequestInputDTO,
)

# --- Shared Kernel Use Cases ---
from src.shared_kernel.application.use_cases.organizational_unit.commands import (
    CreateOrganizationalUnitInputDTO,
    CreateOrganizationalUnitUseCase,
    DeleteOrganizationalUnitUseCase,
    RestoreOrganizationalUnitUseCase,
    UpdateOrganizationalUnitInputDTO,
    UpdateOrganizationalUnitOutputDTO,
    UpdateOrganizationalUnitUseCase,
)
from src.shared_kernel.application.use_cases.organizational_unit.queries import (
    GetOrganizationalUnitByIdUseCase,
    ListOrganizationalUnitUseCase,
)
from src.shared_kernel.domain.entities import OrganizationalUnit
from src.shared_kernel.domain.exceptions import (
    InvalidOrganizationalUnitError,
    OrganizationalUnitNotFoundError,
)

# --- Permissions ---

# --- Permissions ---
require_organizational_unit_create_or_update = PermissionChecker(
    [
        "organizational_unit:create",
        "organizational_unit:update",
    ]
)
require_organizational_unit_delete = PermissionChecker(
    [
        "organizational_unit:delete",
    ]
)
require_organizational_unit_read = PermissionChecker(
    [
        "organizational_unit:read",
    ]
)


# --- Response Models ---
class OrganizationalUnitDetailResponse(BaseModel):
    """
    Response model for Organizational Unit API.
    """

    id: UUID
    code: str
    description: str
    parent_id: UUID | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class OrganizationalUnitResponse(BaseModel):
    """
    Response model for Organizational Unit API.
    """

    id: UUID
    description: str

    model_config = ConfigDict(from_attributes=True)


class PaginatedOrganizationalUnitResponse(
    PaginatedApiResponse[OrganizationalUnitResponse]
):
    """
    Paginated response model for Organizational Unit.
    """


# --- Request Body Models ---
class OrganizationalUnitCreateBody(BaseModel):
    """
    Request model for creating an organizational unit.
    """

    code: str = Field(min_length=3, max_length=10)
    description: str = Field(min_length=3, max_length=100)
    parent_id: UUID | None = None


class OrganizationalUnitUpdateBody(BaseModel):
    """
    Request model for updating an organizational unit.
    """

    code: str = Field(min_length=3, max_length=10)
    description: str = Field(min_length=3, max_length=100)
    parent_id: UUID | None = None


# --- Router ---
router = APIRouter(
    prefix="/organizational-units",
    tags=["Organizational Units"],
    dependencies=[
        Depends(get_current_user),
    ],
)


# --- Endpoints ---
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_organizational_unit_create_or_update)],
)
async def create_organizational_unit(
    request_body: OrganizationalUnitCreateBody,
    repo: OrganizationalUnitRepositoryDep,
    actor: CurrentUserDep,
) -> dict[str, UUID]:
    """
    Create a new organizational unit.
    """

    try:
        use_case = CreateOrganizationalUnitUseCase(repo)

        input_dto = CreateOrganizationalUnitInputDTO(
            actor=actor,
            code=request_body.code,
            description=request_body.description,
            parent_id=request_body.parent_id,
        )
        result = await use_case.execute(input_dto)
        return {"id": result.id}
    except InvalidOrganizationalUnitError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        ) from e


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedOrganizationalUnitResponse,
    dependencies=[Depends(require_organizational_unit_read)],
)
async def list_organizational_units_endpoint(
    repo: OrganizationalUnitRepositoryDep,
    actor: CurrentUserDep,
    description: Annotated[
        str | None, Query(description="Filter by description")
    ] = None,
    sort_by: Annotated[str | None, Query(description="Sort field")] = "description",
    sort_order: Annotated[
        str, Query(enum=["asc", "desc"], description="Sort order")
    ] = "asc",
    offset: Annotated[int, Query(ge=0, description="Offset")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Limit")] = 10,
) -> PaginatedResponseDTO[OrganizationalUnit]:
    """
    List organizational_units with filters, order and pagination.
    """

    filters = {}
    if description:
        filters["description"] = description

    input_dto = ListRequestInputDTO(
        actor=actor,
        filters=filters,
        sort_by=sort_by,
        sort_order=sort_order,
        offset=offset,
        limit=limit,
    )

    use_case = ListOrganizationalUnitUseCase(repo)
    result = await use_case.execute(input_dto)
    return result


@router.get(
    "/{organizational_unit_id}",
    status_code=status.HTTP_200_OK,
    response_model=OrganizationalUnitDetailResponse,
    dependencies=[Depends(require_organizational_unit_read)],
)
async def get_organizational_unit_by_id_endpoint(
    organizational_unit_id: Annotated[
        UUID, Path(description="The organizational unit ID")
    ],
    repo: OrganizationalUnitRepositoryDep,
    actor: CurrentUserDep,
) -> OrganizationalUnit:
    """
    Get an organizational unit by its ID.
    """

    try:
        use_case = GetOrganizationalUnitByIdUseCase(repo)
        input_dto = GetByIdRequestInputDTO(id=organizational_unit_id, actor=actor)
        organizational_unit = await use_case.execute(input_dto)
        return organizational_unit
    except OrganizationalUnitNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        ) from e


@router.put(
    "/{organizational_unit_id}",
    status_code=status.HTTP_200_OK,
    response_model=OrganizationalUnitResponse,
    dependencies=[Depends(require_organizational_unit_create_or_update)],
)
async def update_organizational_unit_endpoint(
    organizational_unit_id: Annotated[
        UUID, Path(description="The organizational unit ID")
    ],
    request_body: OrganizationalUnitUpdateBody,
    repo: OrganizationalUnitRepositoryDep,
    actor: CurrentUserDep,
) -> UpdateOrganizationalUnitOutputDTO:
    """
    Update an existing organizational_unit.
    """

    try:
        use_case = UpdateOrganizationalUnitUseCase(repo)

        input_dto = UpdateOrganizationalUnitInputDTO(
            id=organizational_unit_id,
            code=request_body.code,
            description=request_body.description,
            parent_id=request_body.parent_id,
            actor=actor,
        )

        output_dto = await use_case.execute(input_dto)

        return output_dto
    except OrganizationalUnitNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except InvalidOrganizationalUnitError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        ) from e


@router.delete(
    "/{organizational_unit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_organizational_unit_delete)],
)
async def delete_organizational_unit_endpoint(
    organizational_unit_id: Annotated[
        UUID, Path(description="The organizational unit ID")
    ],
    repo: OrganizationalUnitRepositoryDep,
    actor: CurrentUserDep,
) -> None:
    """
    Delete an existing organizational_unit (soft delete).
    """

    try:
        use_case = DeleteOrganizationalUnitUseCase(repo)
        await use_case.execute(
            DeleteRequestInputDTO(id=organizational_unit_id, actor=actor)
        )
    except OrganizationalUnitNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.patch(
    "/{organizational_unit_id}/restore",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_organizational_unit_delete)],
)
async def restore_organizational_unit_endpoint(
    organizational_unit_id: Annotated[
        UUID, Path(description="The organizational unit ID")
    ],
    repo: OrganizationalUnitRepositoryDep,
    actor: CurrentUserDep,
) -> None:
    """
    Restore a soft-deleted organizational_unit.
    """

    try:
        use_case = RestoreOrganizationalUnitUseCase(repo)
        await use_case.execute(
            RestoreRequestInputDTO(id=organizational_unit_id, actor=actor)
        )
    except OrganizationalUnitNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
