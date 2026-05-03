from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID

from src.core.domain.exceptions import EntityValidationError
from src.planning.domain.entities import Scenario, ScenarioType
from src.planning.domain.exceptions import InvalidScenarioError
from src.planning.domain.repositories import IScenarioRepository

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class CreateScenarioInputDTO:
    """
    Data Transfer Object for input data when creating a new Scenario.
    """

    actor: "User"
    description: str
    scenario_type: ScenarioType
    is_locked: bool = False
    assumptions: str | None = field(default=None)


@dataclass(frozen=True)
class CreateScenarioOutputDTO:
    """
    Data Transfer Object for output data when creating a new Scenario.
    """

    id: UUID


class CreateScenarioUseCase:
    """
    Create a new Scenario.
    """

    def __init__(self, repository: IScenarioRepository) -> None:
        """
        Initialize the CreateScenarioUseCase.
        """

        self._repository = repository

    def execute(
        self,
        input_dto: CreateScenarioInputDTO,
    ) -> CreateScenarioOutputDTO:
        """
        Execute the use case to create a new Scenario.
        """

        try:
            entity = Scenario(
                description=input_dto.description,
                scenario_type=input_dto.scenario_type,
                is_locked=input_dto.is_locked,
                assumptions=input_dto.assumptions,
                tenant_id=input_dto.actor.tenant_id,
            )
            entity.created_by = input_dto.actor.id
            entity.updated_by = input_dto.actor.id
        except EntityValidationError as e:
            raise InvalidScenarioError(f"Invalid input data: {e}") from e

        self._repository.save(entity)
        return CreateScenarioOutputDTO(id=entity.id)
