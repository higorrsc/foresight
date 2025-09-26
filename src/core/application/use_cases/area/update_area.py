from dataclasses import dataclass
from typing import Any

from core.application.use_cases.area import AreaNotFoundError
from core.domain._shared import AbstractRepository
from core.domain.entities import Area


@dataclass
class InputUpdateAreaDTO:
    """
    Data Transfer Object for input data when updating an area.
    """

    id: Any
    description: str


@dataclass
class OutputUpdateAreaDTO:
    """
    Data Transfer Object for output data when updating an area.
    """

    id: Any
    description: str


class UpdateArea:
    """
    Use case for updating an existing area.
    """

    def __init__(self, repository: AbstractRepository[Area]) -> None:
        """
        Initialize the update use case.
        """

        self._repository = repository

    def execute(self, input_dto: InputUpdateAreaDTO) -> OutputUpdateAreaDTO:
        """
        Execute the use case to update an area.
        """

        area = self._repository.get_by_id(input_dto.id)
        if area is None:
            raise AreaNotFoundError(f"Area with id {input_dto.id} not found.")

        try:
            area.update_area(new_description=input_dto.description)
        except ValueError as e:
            raise ValueError(f"Invalid input data: {e}") from e

        self._repository.save(area)
        return OutputUpdateAreaDTO(
            id=area.id,
            description=area.description,
        )
