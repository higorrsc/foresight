from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest

from src.finance.domain.value_objects import CurrencyCode
from src.identity_access_management.domain.entities import User
from src.planning.application.use_cases.scenario.commands import (
    RemoveExchangeRateInputDTO,
    RemoveExchangeRateUseCase,
)
from src.planning.domain.entities import ExchangeRate, Scenario, ScenarioType
from src.planning.domain.exceptions import (
    CannotUpdateLockedScenarioError,
    ExchangeRateNotFoundError,
)
from tests.fakes import ExchangeRateInMemoryRepository, ScenarioInMemoryRepository


class TestRemoveExchangeRateUseCase:
    """
    Test suite for the RemoveExchangeRateUseCase.
    """

    async def test_remove_exchange_rate_success(self, admin_actor: User):
        """
        Test successful removal of an exchange rate.
        """
        scenario_repo = ScenarioInMemoryRepository()
        exchange_rate_repo = ExchangeRateInMemoryRepository()
        use_case = RemoveExchangeRateUseCase(scenario_repo, exchange_rate_repo)

        scenario = Scenario(
            description="Test Scenario",
            scenario_type=ScenarioType.BUDGET,
            assumptions="Some assumptions",
            tenant_id=admin_actor.tenant_id,
        )
        await scenario_repo.save(scenario)

        rate = ExchangeRate(
            scenario_id=scenario.id,
            from_currency=CurrencyCode(value="USD"),
            to_currency=CurrencyCode(value="BRL"),
            rate=Decimal("5.0"),
            effective_date=date.today(),
        )
        await exchange_rate_repo.save(rate)

        input_dto = RemoveExchangeRateInputDTO(
            actor=admin_actor,
            id=rate.id,
        )

        await use_case.execute(input_dto)

        result = await exchange_rate_repo.get_by_id(
            rate.id,
            admin_actor.tenant_id,
        )

        assert result is None

    async def test_remove_exchange_rate_not_found(self, admin_actor: User):
        """
        Test error when exchange rate is not found.
        """
        scenario_repo = ScenarioInMemoryRepository()
        exchange_rate_repo = ExchangeRateInMemoryRepository()
        use_case = RemoveExchangeRateUseCase(scenario_repo, exchange_rate_repo)

        input_dto = RemoveExchangeRateInputDTO(
            actor=admin_actor,
            id=uuid4(),
        )

        with pytest.raises(ExchangeRateNotFoundError):
            await use_case.execute(input_dto)

    async def test_remove_exchange_rate_scenario_locked(self, admin_actor: User):
        """
        Test error when scenario is locked.
        """
        scenario_repo = ScenarioInMemoryRepository()
        exchange_rate_repo = ExchangeRateInMemoryRepository()
        use_case = RemoveExchangeRateUseCase(scenario_repo, exchange_rate_repo)

        scenario = Scenario(
            description="Locked Scenario",
            scenario_type=ScenarioType.BUDGET,
            assumptions="Some assumptions",
            tenant_id=admin_actor.tenant_id,
            is_locked=True,
        )
        await scenario_repo.save(scenario)

        rate = ExchangeRate(
            scenario_id=scenario.id,
            from_currency=CurrencyCode(value="USD"),
            to_currency=CurrencyCode(value="BRL"),
            rate=Decimal("5.0"),
            effective_date=date.today(),
        )
        await exchange_rate_repo.save(rate)

        input_dto = RemoveExchangeRateInputDTO(
            actor=admin_actor,
            id=rate.id,
        )

        with pytest.raises(CannotUpdateLockedScenarioError):
            await use_case.execute(input_dto)
