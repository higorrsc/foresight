from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from src.api.dependencies.database import get_area_repository
from src.core.application._shared.use_cases.generic_delete import DeleteRequestInputDTO
from src.core.application._shared.use_cases.generic_get_by_id import (
    GetByIdRequestInputDTO,
)
from src.core.application.use_cases.area import (
    AreaNotFoundError,
    CreateAreaInputDTO,
    CreateAreaUseCase,
    DeleteAreaUseCase,
    GetAreaByIdUseCase,
    ListAreaUseCase,
    UpdateAreaInputDTO,
    UpdateAreaUseCase,
)
from src.core.infrastructure.repositories.area_repository import AreaRepository


class AreaResponse(BaseModel):
    """
    Response model for API.
    """

    id: UUID
    description: str
    created_at: datetime
    updated_at: datetime


class AreaUpdateBody(BaseModel):
    """
    Request model for update area.
    """

    description: str = Field(
        ...,
        min_length=3,
        max_length=100,
    )


router = APIRouter(
    prefix="/areas",
    tags=["Areas"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_area_endpoint(
    request: CreateAreaInputDTO,
    repo: AreaRepository = Depends(get_area_repository),
):
    """
    Create a new area.
    """

    try:
        use_case = CreateAreaUseCase(repo)
        result = use_case.execute(request)
        return {"id": result.id}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[AreaResponse],
)
def list_areas_endpoint(repo: AreaRepository = Depends(get_area_repository)):
    """
    List all areas.
    """

    use_case = ListAreaUseCase(repo)
    result = use_case.execute()
    return result.data


@router.get(
    "/{area_id}",
    status_code=status.HTTP_200_OK,
    response_model=AreaResponse,
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
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.put(
    "/{area_id}",
    status_code=status.HTTP_200_OK,
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
        input_dto = UpdateAreaInputDTO(
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
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.delete(
    "/{area_id}",
    status_code=status.HTTP_204_NO_CONTENT,
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
