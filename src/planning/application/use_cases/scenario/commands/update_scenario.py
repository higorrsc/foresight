from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID

from src.core.domain.exceptions import EntityValidationError
from src.finance.domain.value_objects import CurrencyCode
from src.planning.domain.entities import ExchangeRate, ScenarioType
from src.planning.domain.exceptions import (
    CannotUpdateLockedScenarioError,
    InvalidScenarioError,
    ScenarioNotFoundError,
)
from src.planning.domain.repositories import IScenarioRepository

from .create_scenario import ExchangeRateInputDTO

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class UpdateScenarioInputDTO:
    """
    Data Transfer Object for input data when updating a existent Scenario.
    """

    actor: "User"
    id: UUID
    description: str
    scenario_type: ScenarioType
    is_locked: bool = False
    assumptions: str | None = field(default=None)
    exchange_rates: list[ExchangeRateInputDTO] | None = field(default=None)


@dataclass(frozen=True)
class UpdateScenarioOutputDTO:
    """
    Data Transfer Object for output data when updating a existent Scenario.
    """

    id: UUID
    description: str


class UpdateScenarioUseCase:
    """
    Use case for updating an existing financial Scenario.
    """

    def __init__(self, repository: IScenarioRepository) -> None:
        """
        Initialize the UpdateScenarioUseCase.
        """

        self._repository = repository

    async def execute(
        self,
        input_dto: UpdateScenarioInputDTO,
    ) -> UpdateScenarioOutputDTO:
        """
        Execute the use case to update an existing Scenario.
        """

        entity = await self._repository.get_by_id(
            entity_id=input_dto.id,
            tenant_id=input_dto.actor.tenant_id,
        )
        if not entity:
            raise ScenarioNotFoundError("Scenario with given ID not found")

        if entity.is_locked:
            raise CannotUpdateLockedScenarioError("Cannot update a locked Scenario")

        try:
            entity.description = input_dto.description
            entity.scenario_type = input_dto.scenario_type
            entity.is_locked = input_dto.is_locked
            entity.assumptions = input_dto.assumptions

            if input_dto.exchange_rates is not None:
                entity.exchange_rates = [
                    ExchangeRate(
                        scenario_id=entity.id,
                        from_currency=CurrencyCode(value=rate.from_currency),
                        to_currency=CurrencyCode(value=rate.to_currency),
                        rate=rate.rate,
                        effective_date=rate.effective_date,
                    )
                    for rate in input_dto.exchange_rates
                ]

            entity.updated_by = input_dto.actor.id
        except EntityValidationError as e:
            raise InvalidScenarioError(f"Invalid input data: {e}") from e

        await self._repository.update(entity)

        return UpdateScenarioOutputDTO(
            id=entity.id,
            description=entity.description,
        )
