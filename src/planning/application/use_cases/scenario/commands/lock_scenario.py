from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from src.core.domain.exceptions import EntityValidationError
from src.planning.domain.exceptions import (
    InvalidScenarioError,
    ScenarioAlreadyLockedError,
    ScenarioNotFoundError,
)
from src.planning.domain.repositories import IScenarioRepository

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class LockScenarioInputDTO:
    """
    Data Transfer Object for input data when updating a existent Scenario.
    """

    actor: "User"
    id: UUID


class LockScenarioUseCase:
    """
    Use case for updating an existing financial Scenario.
    """

    def __init__(self, repository: IScenarioRepository) -> None:
        """
        Initialize the LockScenarioUseCase.
        """

        self._repository = repository

    def execute(
        self,
        input_dto: LockScenarioInputDTO,
    ) -> None:
        """
        Execute the use case to update an existing Scenario.
        """

        entity = self._repository.get_by_id(
            entity_id=input_dto.id,
            tenant_id=input_dto.actor.tenant_id,
        )

        if not entity:
            raise ScenarioNotFoundError("Scenario with given ID not found")

        if entity.is_locked:
            raise ScenarioAlreadyLockedError("Scenario is already locked")

        try:
            entity.lock()
            entity.updated_by = input_dto.actor.id
        except EntityValidationError as e:
            raise InvalidScenarioError(f"Invalid input data: {e}") from e

        self._repository.update(entity)
