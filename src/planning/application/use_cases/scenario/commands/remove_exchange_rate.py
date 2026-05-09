from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from src.identity_access_management.domain.constants import AppPermission
from src.identity_access_management.domain.exceptions import InsufficientPermissionError
from src.planning.domain.exceptions import (
    CannotUpdateLockedScenarioError,
    ExchangeRateNotFoundError,
    ScenarioNotFoundError,
)
from src.planning.domain.repositories import (
    IExchangeRateRepository,
    IScenarioRepository,
)

if TYPE_CHECKING:
    from src.identity_access_management.domain.entities import User


@dataclass(frozen=True)
class RemoveExchangeRateInputDTO:
    """
    Data Transfer Object for removing an exchange rate.
    """

    actor: "User"
    id: UUID


class RemoveExchangeRateUseCase:
    """
    Use case for removing an exchange rate.
    """

    def __init__(
        self,
        scenario_repository: IScenarioRepository,
        exchange_rate_repository: IExchangeRateRepository,
    ) -> None:
        self._scenario_repository = scenario_repository
        self._exchange_rate_repository = exchange_rate_repository

    async def execute(self, input_dto: RemoveExchangeRateInputDTO) -> None:
        """
        Execute the use case to remove an exchange rate.
        """

        if AppPermission.SCENARIO_UPDATE not in input_dto.actor.permissions:
            raise InsufficientPermissionError(
                "User does not have permission to update scenario."
            )

        exchange_rate = await self._exchange_rate_repository.get_by_id(
            input_dto.id,
            tenant_id=input_dto.actor.tenant_id,
        )

        if not exchange_rate:
            raise ExchangeRateNotFoundError(
                f"Exchange rate with id={input_dto.id} not found."
            )

        scenario = await self._scenario_repository.get_by_id(
            exchange_rate.scenario_id,
            tenant_id=input_dto.actor.tenant_id,
        )

        if not scenario:
            raise ScenarioNotFoundError(
                f"Scenario with id={exchange_rate.scenario_id} not found."
            )

        if scenario.is_locked:
            raise CannotUpdateLockedScenarioError(
                f"Scenario with id={exchange_rate.scenario_id} is locked."
            )

        await self._exchange_rate_repository.delete(
            input_dto.id,
            tenant_id=input_dto.actor.tenant_id,
        )
