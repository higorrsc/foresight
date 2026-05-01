from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID

from src.core.domain.exceptions import EntityValidationError
from src.shared_kernel.application.use_cases.financial_scenario import (
    CannotUpdateLockedFinancialScenarioError,
    FinancialScenarioNotFoundError,
    InvalidFinancialScenarioError,
)
from src.shared_kernel.domain.entities import ScenarioType
from src.shared_kernel.domain.repositories import IFinancialScenarioRepository

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class UpdateFinancialScenarioInputDTO:
    """
    Data Transfer Object for input data when updating a existent Financial Scenario.
    """

    actor: "User"
    id: UUID
    description: str
    scenario_type: ScenarioType
    is_locked: bool = False
    assumptions: str | None = field(default=None)


@dataclass(frozen=True)
class UpdateFinancialScenarioOutputDTO:
    """
    Data Transfer Object for output data when updating a existent Financial Scenario.
    """

    id: UUID
    description: str


class UpdateFinancialScenarioUseCase:
    """
    Use case for updating an existing financial Scenario.
    """

    def __init__(self, repository: IFinancialScenarioRepository) -> None:
        """
        Initialize the UpdateFinancialScenarioUseCase.
        """

        self._repository = repository

    def execute(
        self,
        input_dto: UpdateFinancialScenarioInputDTO,
    ) -> UpdateFinancialScenarioOutputDTO:
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

        if entity.is_locked:
            raise CannotUpdateLockedFinancialScenarioError(
                "Cannot update a locked Financial Scenario"
            )

        try:
            entity.description = input_dto.description
            entity.scenario_type = input_dto.scenario_type
            entity.is_locked = input_dto.is_locked
            entity.assumptions = input_dto.assumptions
            entity.updated_by = input_dto.actor.id
        except EntityValidationError as e:
            raise InvalidFinancialScenarioError(f"Invalid input data: {e}") from e

        self._repository.update(entity)
        return UpdateFinancialScenarioOutputDTO(
            id=entity.id,
            description=entity.description,
        )
