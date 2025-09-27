from typing import Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.core.application._shared.use_cases.generic_delete import InputDeleteRequestDTO
from src.core.application.use_cases.area import (
    CreateAreaUseCase,
    DeleteAreaUseCase,
    ListAreaUseCase,
    UpdateAreaUseCase,
)
from src.core.application.use_cases.area.create_area import InputCreateAreaUseCaseDTO
from src.core.application.use_cases.area.exceptions import AreaNotFoundError
from src.core.application.use_cases.area.update_area import InputUpdateAreaUseCaseDTO
from src.core.domain.entities.area import Area
from src.core.infrastructure.repositories._shared import InMemoryRepository

area_repository = InMemoryRepository[Area]()

create_area_use_case = CreateAreaUseCase(area_repository)
list_area_use_case = ListAreaUseCase(area_repository)
update_area_use_case = UpdateAreaUseCase(area_repository)
delete_area_use_case = DeleteAreaUseCase(area_repository)

router = APIRouter(
    prefix="/areas",
    tags=["Areas"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
def create_area_endpoint(request: InputCreateAreaUseCaseDTO):
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
        }
        for area in areas.data
    ]


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

        input_dto = InputUpdateAreaUseCaseDTO(
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
        delete_area_use_case.execute(InputDeleteRequestDTO(area_id))
    except AreaNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
