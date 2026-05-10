from decimal import Decimal
from uuid import uuid4

import pytest

from src.identity_access_management.domain.entities import User
from src.identity_access_management.domain.exceptions import InsufficientPermissionError
from src.planning.application.use_cases.scenario.commands import (
    AddExchangeRateInputDTO,
    AddExchangeRateToScenarioUseCase,
)
from src.planning.domain.entities import Scenario, ScenarioType
from src.planning.domain.exceptions import (
    CannotUpdateLockedScenarioError,
    ScenarioNotFoundError,
)
from tests.fakes import ExchangeRateInMemoryRepository, ScenarioInMemoryRepository


class TestAddExchangeRateToScenarioUseCase:
    """
    Test suite for the AddExchangeRateToScenarioUseCase.
    """

    async def test_add_exchange_rate_success(self, admin_actor: User):
        """
        Test successful addition of an exchange rate to a scenario.
        """
        scenario_repo = ScenarioInMemoryRepository()
        exchange_rate_repo = ExchangeRateInMemoryRepository()
        use_case = AddExchangeRateToScenarioUseCase(scenario_repo, exchange_rate_repo)

        scenario = Scenario(
            description="Test Scenario",
            scenario_type=ScenarioType.BUDGET,
            assumptions="Some assumptions",
            tenant_id=admin_actor.tenant_id,
        )
        await scenario_repo.save(scenario)

        input_dto = AddExchangeRateInputDTO(
            actor=admin_actor,
            scenario_id=scenario.id,
            from_currency="USD",
            to_currency="BRL",
            rate=Decimal("5.25"),
        )

        result = await use_case.execute(input_dto)

        assert result.id is not None
        saved_rate = await exchange_rate_repo.get_by_id(
            result.id, admin_actor.tenant_id
        )
        assert saved_rate.scenario_id == scenario.id  # type: ignore
        assert str(saved_rate.from_currency) == "USD"  # type: ignore
        assert saved_rate.rate == Decimal("5.25")  # type: ignore

    async def test_add_exchange_rate_scenario_not_found(self, admin_actor: User):
        """
        Test error when scenario is not found.
        """
        scenario_repo = ScenarioInMemoryRepository()
        exchange_rate_repo = ExchangeRateInMemoryRepository()
        use_case = AddExchangeRateToScenarioUseCase(scenario_repo, exchange_rate_repo)

        input_dto = AddExchangeRateInputDTO(
            actor=admin_actor,
            scenario_id=uuid4(),
            from_currency="USD",
            to_currency="BRL",
            rate=Decimal("5.25"),
        )

        with pytest.raises(ScenarioNotFoundError):
            await use_case.execute(input_dto)

    async def test_add_exchange_rate_scenario_locked(self, admin_actor: User):
        """
        Test error when scenario is locked.
        """
        scenario_repo = ScenarioInMemoryRepository()
        exchange_rate_repo = ExchangeRateInMemoryRepository()
        use_case = AddExchangeRateToScenarioUseCase(scenario_repo, exchange_rate_repo)

        scenario = Scenario(
            description="Locked Scenario",
            scenario_type=ScenarioType.BUDGET,
            assumptions="Some assumptions",
            tenant_id=admin_actor.tenant_id,
            is_locked=True,
        )
        await scenario_repo.save(scenario)

        input_dto = AddExchangeRateInputDTO(
            actor=admin_actor,
            scenario_id=scenario.id,
            from_currency="USD",
            to_currency="BRL",
            rate=Decimal("5.25"),
        )

        with pytest.raises(CannotUpdateLockedScenarioError):
            await use_case.execute(input_dto)

    async def test_add_exchange_rate_insufficient_permission(self, guest_actor: User):
        """
        Test error when user has insufficient permission.
        """
        scenario_repo = ScenarioInMemoryRepository()
        exchange_rate_repo = ExchangeRateInMemoryRepository()
        use_case = AddExchangeRateToScenarioUseCase(scenario_repo, exchange_rate_repo)

        input_dto = AddExchangeRateInputDTO(
            actor=guest_actor,
            scenario_id=uuid4(),
            from_currency="USD",
            to_currency="BRL",
            rate=Decimal("5.25"),
        )

        with pytest.raises(InsufficientPermissionError):
            await use_case.execute(input_dto)
