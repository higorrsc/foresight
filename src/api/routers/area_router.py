from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from src.api.dependencies.auth import get_current_user
from src.api.dependencies.authorization import PermissionChecker
from src.api.dependencies.database import get_area_repository
from src.api.routers._shared import PaginationMetaResponse
from src.core.application._shared.use_cases.commands import (
    CreateDescribedEntityInputDTO,
    DeleteRequestInputDTO,
    RestoreRequestInputDTO,
    UpdateDescribedEntityInputDTO,
)
from src.core.application._shared.use_cases.queries import (
    GetByIdRequestInputDTO,
    ListRequestInputDTO,
)
from src.core.application.use_cases.area import AreaNotFoundError, InvalidAreaError
from src.core.application.use_cases.area.commands import (
    CreateAreaUseCase,
    DeleteAreaUseCase,
    RestoreAreaUseCase,
    UpdateAreaUseCase,
)
from src.core.application.use_cases.area.queries import (
    GetAreaByIdUseCase,
    ListAreaUseCase,
)
from src.core.infrastructure.repositories.area_repository import AreaRepository

require_area_create_or_update = PermissionChecker(["area:create", "area:update"])
require_area_delete = PermissionChecker(["area:delete"])
require_area_read = PermissionChecker(["area:read"])


class AreaResponse(BaseModel):
    """
    Response model for API.
    """

    id: UUID
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class AreaUpdateBody(BaseModel):
    """
    Request model for update area.
    """

    description: str = Field(
        ...,
        min_length=3,
        max_length=100,
    )


class PaginatedAreaResponse(BaseModel):
    """
    Response model for API.
    """

    data: List[AreaResponse]
    meta: PaginationMetaResponse


router = APIRouter(
    prefix="/areas",
    tags=["Areas"],
    dependencies=[
        Depends(get_current_user),
    ],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_area_create_or_update)],
)
def create_area_endpoint(
    request: CreateDescribedEntityInputDTO,
    repo: AreaRepository = Depends(get_area_repository),
):
    """
    Create a new area.
    """

    try:
        use_case = CreateAreaUseCase(repo)
        result = use_case.execute(request)
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
def list_areas_endpoint(
    repo: AreaRepository = Depends(get_area_repository),
    description: Optional[str] = Query(
        None,
        description="Filtrar por parte da descrição",
    ),
    sort_by: Optional[str] = Query(
        "description",
        description="Campo para ordenação",
    ),
    sort_order: str = Query(
        "asc",
        enum=["asc", "desc"],
        description="Ordem da ordenação",
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Offset para paginação",
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Limite de registos por página",
    ),
):
    """
    List areas with filters, order and pagination.
    """

    filters = {}
    if description:
        filters["description"] = description

    input_dto = ListRequestInputDTO(
        filters=filters,
        sort_by=sort_by,
        sort_order=sort_order,
        offset=offset,
        limit=limit,
    )

    use_case = ListAreaUseCase(repo)
    result = use_case.execute(input_dto)
    return result


@router.get(
    "/{area_id}",
    status_code=status.HTTP_200_OK,
    response_model=AreaResponse,
    dependencies=[Depends(require_area_read)],
)
def get_area_by_id_endpoint(
    area_id: UUID,
    repo: AreaRepository = Depends(get_area_repository),
):
    """
    Getting an area by its ID.
    """

    try:
        use_case = GetAreaByIdUseCase(repo)
        input_dto = GetByIdRequestInputDTO(id=area_id)
        area = use_case.execute(input_dto)
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
def update_area_endpoint(
    area_id: UUID,
    request_body: AreaUpdateBody,
    repo: AreaRepository = Depends(get_area_repository),
):
    """
    Update an existing area.
    """

    try:
        use_case = UpdateAreaUseCase(repo)
        input_dto = UpdateDescribedEntityInputDTO(
            id=area_id,
            description=request_body.description,
        )
        output_dto = use_case.execute(input_dto)
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
def delete_area_endpoint(
    area_id: UUID,
    repo: AreaRepository = Depends(get_area_repository),
):
    """
    Delete an existing area.
    """

    try:
        use_case = DeleteAreaUseCase(repo)
        use_case.execute(DeleteRequestInputDTO(area_id))
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
def restore_area_endpoint(
    area_id: UUID,
    repo: AreaRepository = Depends(get_area_repository),
):
    """
    Restore an existing area.
    """

    try:
        use_case = RestoreAreaUseCase(repo)
        use_case.execute(RestoreRequestInputDTO(area_id))
    except AreaNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
