from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel, ConfigDict, Field

from src.api.dependencies import (
    AreaRepositoryDep,
    CurrentUserDep,
    PermissionChecker,
    get_current_user,
)
from src.api.v1.routers._shared import PaginatedApiResponse
from src.core.application import PaginatedResponseDTO
from src.core.application.use_cases.commands import (
    CreateDescribedEntityInputDTO,
    DeleteRequestInputDTO,
    RestoreRequestInputDTO,
    UpdateDescribedEntityInputDTO,
)
from src.core.application.use_cases.queries import (
    GetByIdRequestInputDTO,
    ListRequestInputDTO,
)

# --- Core Use Cases ---
from src.shared_kernel.application.use_cases.area.commands import (
    CreateAreaUseCase,
    DeleteAreaUseCase,
    RestoreAreaUseCase,
    UpdateAreaUseCase,
)
from src.shared_kernel.application.use_cases.area.queries import (
    GetAreaByIdUseCase,
    ListAreaUseCase,
)
from src.shared_kernel.domain.entities import Area
from src.shared_kernel.domain.exceptions import (
    AreaNotFoundError,
    InvalidAreaError,
)

# --- Permissions ---

# --- Permissions ---
require_area_create_or_update = PermissionChecker(["area:create", "area:update"])
require_area_delete = PermissionChecker(["area:delete"])
require_area_read = PermissionChecker(["area:read"])


# --- Response Models ---
class AreaResponse(BaseModel):
    """
    Response model for Area API.
    """

    id: UUID
    description: str

    model_config = ConfigDict(from_attributes=True)


class AreaResponseDetail(BaseModel):
    """
    Response model for Area API.
    """

    id: UUID
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class PaginatedAreaResponse(PaginatedApiResponse[AreaResponse]):
    """
    Paginated response model for Area.
    """


# --- Request Body Models ---
class AreaCreateBody(BaseModel):
    """
    Request model for creating an area.
    """

    description: str = Field(min_length=3, max_length=100)


class AreaUpdateBody(BaseModel):
    """
    Request model for updating an area.
    """

    description: str = Field(min_length=3, max_length=100)


# --- Router ---
router = APIRouter(
    prefix="/areas",
    tags=["Areas"],
    dependencies=[
        Depends(get_current_user),
    ],
)


# --- Endpoints ---
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_area_create_or_update)],
)
async def create_area_endpoint(
    request_body: AreaCreateBody,
    repo: AreaRepositoryDep,
    actor: CurrentUserDep,
) -> dict[str, UUID]:
    """
    Create a new area.
    """

    try:
        use_case = CreateAreaUseCase(repo)

        input_dto = CreateDescribedEntityInputDTO(
            actor=actor, description=request_body.description
        )

        result = await use_case.execute(input_dto)
        return {"id": result.id}
    except InvalidAreaError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        ) from e


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedAreaResponse,
    dependencies=[Depends(require_area_read)],
)
async def list_areas_endpoint(
    repo: AreaRepositoryDep,
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
) -> PaginatedResponseDTO[Area]:
    """
    List areas with filters, order and pagination.
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

    use_case = ListAreaUseCase(repo)
    result = await use_case.execute(input_dto)
    return result


@router.get(
    "/{area_id}",
    status_code=status.HTTP_200_OK,
    response_model=AreaResponseDetail,
    dependencies=[Depends(require_area_read)],
)
async def get_area_by_id_endpoint(
    area_id: Annotated[UUID, Path(description="The area ID")],
    repo: AreaRepositoryDep,
    actor: CurrentUserDep,
) -> Area:
    """
    Get an area by its ID.
    """

    try:
        use_case = GetAreaByIdUseCase(repo)
        input_dto = GetByIdRequestInputDTO(id=area_id, actor=actor)
        area = await use_case.execute(input_dto)
        return area
    except AreaNotFoundError as e:
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
    "/{area_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_area_create_or_update)],
)
async def update_area_endpoint(
    area_id: Annotated[UUID, Path(description="The area ID")],
    request_body: AreaUpdateBody,
    repo: AreaRepositoryDep,
    actor: CurrentUserDep,
) -> dict[str, UUID | str]:
    """
    Update an existing area.
    """

    try:
        use_case = UpdateAreaUseCase(repo)

        input_dto = UpdateDescribedEntityInputDTO(
            id=area_id,
            actor=actor,
            description=request_body.description,
        )

        output_dto = await use_case.execute(input_dto)
        return {
            "id": output_dto.id,
            "description": output_dto.description,
        }
    except AreaNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except InvalidAreaError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e),
        ) from e


@router.delete(
    "/{area_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_area_delete)],
)
async def delete_area_endpoint(
    area_id: Annotated[UUID, Path(description="The area ID")],
    repo: AreaRepositoryDep,
    actor: CurrentUserDep,
) -> None:
    """
    Delete an existing area (soft delete).
    """

    try:
        use_case = DeleteAreaUseCase(repo)
        await use_case.execute(DeleteRequestInputDTO(id=area_id, actor=actor))
    except AreaNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.patch(
    "/{area_id}/restore",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_area_delete)],
)
async def restore_area_endpoint(
    area_id: Annotated[UUID, Path(description="The area ID")],
    repo: AreaRepositoryDep,
    actor: CurrentUserDep,
) -> None:
    """
    Restore a soft-deleted area.
    """

    try:
        use_case = RestoreAreaUseCase(repo)
        await use_case.execute(RestoreRequestInputDTO(id=area_id, actor=actor))
    except AreaNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
