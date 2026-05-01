from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID

from src.core.domain.exceptions import EntityValidationError
from src.shared_kernel.application.use_cases.financial_scenario.exceptions import (
    InvalidFinancialScenarioError,
)
from src.shared_kernel.domain.entities import FinancialScenario, ScenarioType
from src.shared_kernel.domain.repositories import IFinancialScenarioRepository

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class CreateFinancialScenarioInputDTO:
    """
    Data Transfer Object for input data when creating a new Financial Scenario.
    """

    actor: "User"
    description: str
    scenario_type: ScenarioType
    is_locked: bool = False
    assumptions: str | None = field(default=None)


@dataclass(frozen=True)
class CreateFinancialScenarioOutputDTO:
    """
    Data Transfer Object for output data when creating a new Financial Scenario.
    """

    id: UUID


class CreateFinancialScenarioUseCase:
    """
    Create a new Financial Scenario.
    """

    def __init__(self, repository: IFinancialScenarioRepository) -> None:
        """
        Initialize the CreateFinancialScenarioUseCase.
        """

        self._repository = repository

    def execute(
        self,
        input_dto: CreateFinancialScenarioInputDTO,
    ) -> CreateFinancialScenarioOutputDTO:
        """
        Execute the use case to create a new Financial Scenario.
        """

        try:
            entity = FinancialScenario(
                description=input_dto.description,
                scenario_type=input_dto.scenario_type,
                is_locked=input_dto.is_locked,
                assumptions=input_dto.assumptions,
                tenant_id=input_dto.actor.tenant_id,
            )
            entity.created_by = input_dto.actor.id
            entity.updated_by = input_dto.actor.id
        except EntityValidationError as e:
            raise InvalidFinancialScenarioError(f"Invalid input data: {e}") from e

        self._repository.save(entity)
        return CreateFinancialScenarioOutputDTO(id=entity.id)
