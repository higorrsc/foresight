from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, Type, TypeVar
from uuid import UUID, uuid4

from src.core.domain import AbstractRepository, EntityValidationError
from src.core.domain.entities import DescribedEntity

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User

T = TypeVar("T", bound=DescribedEntity)


@dataclass(frozen=True)
class CreateDescribedEntityInputDTO:
    """
    Data Transfer Object for input data when creating a new entity.
    """

    actor: "User"
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
                tenant_id=input_dto.actor.tenant_id,
                description=input_dto.description,
            )
        except EntityValidationError as e:
            raise self._invalid_data_exception(f"Invalid input data: {e}") from e

        self._repository.save(entity)
        return CreateDescribedEntityOutputDTO(id=entity.id)
