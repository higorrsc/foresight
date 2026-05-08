from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from src.finance.domain.value_objects import CurrencyCode
from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.exceptions import InsufficientPermissionError
from src.planning.domain.entities import ExchangeRate
from src.planning.domain.exceptions import (
    CannotUpdateLockedScenarioError,
    ScenarioNotFoundError,
)
from src.planning.domain.repositories import (
    IExchangeRateRepository,
    IScenarioRepository,
)

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class AddExchangeRateInputDTO:
    """
    Data Transfer Object for adding an exchange rate to a scenario.
    """

    actor: "User"
    scenario_id: UUID
    from_currency: str
    to_currency: str
    rate: Decimal


@dataclass(frozen=True)
class AddExchangeRateOutputDTO:
    """
    Data Transfer Object for the output of adding an exchange rate.
    """

    id: UUID


class AddExchangeRateToScenarioUseCase:
    """
    Use case for adding an exchange rate to a scenario.
    """

    def __init__(
        self,
        scenario_repository: IScenarioRepository,
        exchange_rate_repository: IExchangeRateRepository,
    ) -> None:
        self._scenario_repository = scenario_repository
        self._exchange_rate_repository = exchange_rate_repository

    def execute(self, input_dto: AddExchangeRateInputDTO) -> AddExchangeRateOutputDTO:
        """
        Execute the use case to add an exchange rate to a scenario.
        """

        if AppPermission.SCENARIO_UPDATE not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to update scenario."
            )

        scenario = self._scenario_repository.get_by_id(
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

        exchange_rate = ExchangeRate(
            scenario_id=input_dto.scenario_id,
            from_currency=CurrencyCode(value=input_dto.from_currency),
            to_currency=CurrencyCode(value=input_dto.to_currency),
            rate=input_dto.rate,
        )

        self._exchange_rate_repository.save(exchange_rate)

        return AddExchangeRateOutputDTO(id=exchange_rate.id)
