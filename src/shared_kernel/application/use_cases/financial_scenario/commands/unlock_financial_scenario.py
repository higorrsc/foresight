from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from src.core.domain.exceptions import EntityValidationError
from src.shared_kernel.application.use_cases.financial_scenario import (
    FinancialScenarioNotFoundError,
    InvalidFinancialScenarioError,
)
from src.shared_kernel.application.use_cases.financial_scenario.exceptions import (
    FinancialScenarioAlreadyUnlockedError,
)
from src.shared_kernel.domain.repositories import IFinancialScenarioRepository

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class UnlockFinancialScenarioInputDTO:
    """
    Data Transfer Object for input data when updating a existent Financial Scenario.
    """

    actor: "User"
    id: UUID


class UnlockFinancialScenarioUseCase:
    """
    Use case for updating an existing financial Scenario.
    """

    def __init__(self, repository: IFinancialScenarioRepository) -> None:
        """
        Initialize the UnlockFinancialScenarioUseCase.
        """

        self._repository = repository

    def execute(
        self,
        input_dto: UnlockFinancialScenarioInputDTO,
    ) -> None:
        """
        Execute the use case to update an existing Financial Scenario.
        """

        entity = self._repository.get_by_id(
            entity_id=input_dto.id,
            tenant_id=input_dto.actor.tenant_id,
        )

        if not entity:
            raise FinancialScenarioNotFoundError(
                "Financial Scenario with given ID not found"
            )

        if not entity.is_locked:
            raise FinancialScenarioAlreadyUnlockedError(
                "Financial Scenario is already unlocked"
            )

        try:
            entity.unlock()
            entity.updated_by = input_dto.actor.id
        except EntityValidationError as e:
            raise InvalidFinancialScenarioError(f"Invalid input data: {e}") from e

        self._repository.update(entity)
