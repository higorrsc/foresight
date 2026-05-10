from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from src.finance.domain.value_objects import CurrencyCode
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.exceptions import InsufficientPermissionError
from src.planning.domain.entities import ExchangeRate
from src.planning.domain.exceptions import (
    CannotUpdateLockedScenarioError,
    ScenarioNotFoundError,
)
from src.planning.domain.repositories import (
    IScenarioRepository,
)

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass
class ExchangeRateEntryDTO:
    """
    Data Transfer Object for an exchange rate entry.
    """

    effective_date: date
    rate: Decimal


@dataclass(frozen=True)
class AddExchangeRateInputDTO:
    """
    Data Transfer Object for adding an exchange rate to a scenario.
    """

    actor: "User"
    scenario_id: UUID
    from_currency: str
    to_currency: str
    exchange: list[ExchangeRateEntryDTO]


@dataclass(frozen=True)
class AddExchangeRateOutputDTO:
    """
    Data Transfer Object for the output of adding an exchange rate.
    """

    scenario_id: UUID
    inserted_count: int


class AddExchangeRateToScenarioUseCase:
    """
    Use case for adding an exchange rate to a scenario.
    """

    def __init__(
        self,
        scenario_repository: IScenarioRepository,
    ) -> None:
        self._scenario_repository = scenario_repository

    async def execute(
        self,
        input_dto: AddExchangeRateInputDTO,
    ) -> AddExchangeRateOutputDTO:
        """
        Execute the use case to add an exchange rate to a scenario.
        """

        if AppPermission.SCENARIO_UPDATE not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to update scenario."
            )

        scenario = await self._scenario_repository.get_by_id(
            input_dto.scenario_id,
            tenant_id=input_dto.actor.tenant_id,
        )

        if not scenario:
            raise ScenarioNotFoundError(
                f"Scenario with id={input_dto.scenario_id} not found."
            )

        if scenario.is_locked:
            raise CannotUpdateLockedScenarioError(
                f"Scenario with id={input_dto.scenario_id} is locked."
            )

        from_curr = CurrencyCode(value=input_dto.from_currency)
        to_curr = CurrencyCode(value=input_dto.to_currency)

        for entry in input_dto.exchange:
            rate_entity = ExchangeRate(
                id=uuid4(),
                scenario_id=input_dto.scenario_id,
                from_currency=from_curr,
                to_currency=to_curr,
                effective_date=entry.effective_date,
                rate=entry.rate,
            )

            scenario.add_exchange_rate(rate_entity)

        await self._scenario_repository.update(scenario)

        return AddExchangeRateOutputDTO(
            scenario_id=scenario.id,
            inserted_count=len(input_dto.exchange),
        )
