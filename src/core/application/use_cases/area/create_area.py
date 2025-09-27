from dataclasses import dataclass, field
from uuid import UUID, uuid4

from src.core.domain._shared import AbstractRepository
from src.core.domain.entities import Area


@dataclass
class InputCreateAreaDTO:
    """
    Data Transfer Object for input data when creating a new area.
    """

    description: str
    id: UUID = field(default_factory=uuid4)


@dataclass
class OutputCreateAreaDTO:
    """
    Data Transfer Object for output data when creating a new area.
    """

    id: UUID


class CreateAreaUseCase:
    """
    Create a new area.
    """

    def __init__(self, repository: AbstractRepository[Area]) -> None:
        """
        Initialize the CreateAreaUseCase.
        """

        self._repository = repository

    def execute(self, input_dto: InputCreateAreaDTO) -> OutputCreateAreaDTO:
        """
        Execute the use case to create a new area.
        """

        try:
            area = Area(
                id=input_dto.id,
                description=input_dto.description,
            )
        except ValueError as e:
            raise ValueError(f"Invalid input data: {e}") from e

        self._repository.save(area)
        return OutputCreateAreaDTO(id=area.id)
