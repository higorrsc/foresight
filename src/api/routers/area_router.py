from typing import Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

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
from src.core.domain.entities.area import Area
from src.core.infrastructure.repositories._shared import InMemoryRepository

area_repository = InMemoryRepository[Area]()

create_area_use_case = CreateAreaUseCase(area_repository)
list_area_use_case = ListAreaUseCase(area_repository)
update_area_use_case = UpdateAreaUseCase(area_repository)
delete_area_use_case = DeleteAreaUseCase(area_repository)
get_area_by_id_use_case = GetAreaByIdUseCase(area_repository)

router = APIRouter(
    prefix="/areas",
    tags=["Areas"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
def create_area_endpoint(request: CreateAreaInputDTO):
    """
    Create a new area.
    """

    try:
        result = create_area_use_case.execute(request)
        return {"id": result.id}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
def list_areas_endpoint():
    """
    List all areas.
    """

    areas = list_area_use_case.execute()
    return [
        {
            "id": area.id,
            "description": area.description,
            "created_at": area.created_at,
            "updated_at": area.updated_at,
        }
        for area in areas.data
    ]


@router.get(
    "/{area_id}",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
def get_area_by_id_endpoint(area_id: UUID):
    """
    Getting an area by its ID.
    """

    try:
        input_dto = GetByIdRequestInputDTO(id=area_id)

        output_dto = get_area_by_id_use_case.execute(input_dto)
        return {
            "id": output_dto.id,
            "description": output_dto.description,
            "created_at": output_dto.created_at,
            "updated_at": output_dto.updated_at,
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


@router.put(
    "/{area_id}",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
def update_area_endpoint(area_id: UUID, request_body: Dict):
    """
    Update an existing area.
    """

    try:
        description = request_body.get("description")
        if description is None:
            raise ValueError("Description is required")

        input_dto = UpdateAreaInputDTO(
            id=area_id,
            description=description,
        )

        output_dto = update_area_use_case.execute(input_dto)
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
    response_model=None,
)
def delete_area_endpoint(area_id: UUID):
    """
    Delete an existing area.
    """

    try:
        delete_area_use_case.execute(DeleteRequestInputDTO(area_id))
    except AreaNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
