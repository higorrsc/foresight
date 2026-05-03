from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from src.core.domain.exceptions import EntityValidationError
from src.planning.domain.exceptions import (
    InvalidScenarioError,
    ScenarioAlreadyUnlockedError,
    ScenarioNotFoundError,
)
from src.planning.domain.repositories import IScenarioRepository

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class UnlockScenarioInputDTO:
    """
    Data Transfer Object for input data when updating a existent Scenario.
    """

    actor: "User"
    id: UUID


class UnlockScenarioUseCase:
    """
    Use case for updating an existing financial Scenario.
    """

    def __init__(self, repository: IScenarioRepository) -> None:
        """
        Initialize the UnlockScenarioUseCase.
        """

        self._repository = repository

    def execute(
        self,
        input_dto: UnlockScenarioInputDTO,
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

        if not entity.is_locked:
            raise ScenarioAlreadyUnlockedError("Scenario is already unlocked")

        try:
            entity.unlock()
            entity.updated_by = input_dto.actor.id
        except EntityValidationError as e:
            raise InvalidScenarioError(f"Invalid input data: {e}") from e

        self._repository.update(entity)
