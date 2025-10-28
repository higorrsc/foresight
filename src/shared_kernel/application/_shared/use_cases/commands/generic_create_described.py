from dataclasses import dataclass, field
from typing import Generic, Type, TypeVar
from uuid import UUID, uuid4

from src.shared_kernel.domain._shared import AbstractRepository, EntityValidationError
from src.shared_kernel.domain._shared.entities import DescribedEntity

T = TypeVar("T", bound=DescribedEntity)


@dataclass(frozen=True)
class CreateDescribedEntityInputDTO:
    """
    Data Transfer Object for input data when creating a new entity.
    """

    description: str
    id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True)
class CreateDescribedEntityOutputDTO:
    """
    Data Transfer Object for output data when creating a new entity.
    """

    id: UUID


class CreateDescribedEntityUseCase(Generic[T]):
    """
    Create a new entity.
    """

    def __init__(
        self,
        repository: AbstractRepository[T],
        entity_cls: Type[T],
        invalid_data_exception: Type[Exception],
    ) -> None:
        """
        Initialize the CreateDescribedEntityUseCase.
        """

        self._repository = repository
        self._entity_cls = entity_cls
        self._invalid_data_exception = invalid_data_exception

    def execute(
        self,
        input_dto: CreateDescribedEntityInputDTO,
    ) -> CreateDescribedEntityOutputDTO:
        """
        Execute the use case to create a new entity.
        """

        try:
            entity = self._entity_cls(
                id=input_dto.id,
                description=input_dto.description,
            )
        except EntityValidationError as e:
            raise self._invalid_data_exception(f"Invalid input data: {e}") from e

        self._repository.save(entity)
        return CreateDescribedEntityOutputDTO(id=entity.id)
