from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest

from src.identity_access_management.domain.entities import User
from src.planning.application.use_cases.scenario.commands import (
    ExchangeRateInputDTO,
    UpdateScenarioInputDTO,
    UpdateScenarioUseCase,
)
from src.planning.domain.entities import Scenario, ScenarioType
from src.planning.domain.exceptions import (
    CannotUpdateLockedScenarioError,
    ScenarioNotFoundError,
)
from tests.fakes import ScenarioInMemoryRepository


class TestUpdateScenarioUseCase:
    """
    Test suite for the UpdateScenarioUseCase.
    """

    async def test_update_scenario_success(self, admin_actor: User):
        """
        Test successful update of a financial scenario.
        """
        repository = ScenarioInMemoryRepository()
        scenario = Scenario(
            description="Old Description",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
        )
        await repository.save(scenario)

        use_case = UpdateScenarioUseCase(repository)
        input_dto = UpdateScenarioInputDTO(
            actor=admin_actor,
            id=scenario.id,
            description="New Description",
            scenario_type=ScenarioType.FORECAST,
            is_locked=False,
        )

        result = await use_case.execute(input_dto)

        assert result.description == "New Description"
        updated_scenario = await repository.get_by_id(
            scenario.id, admin_actor.tenant_id
        )
        assert updated_scenario.description == "New Description"  # type: ignore
        assert updated_scenario.scenario_type == ScenarioType.FORECAST  # type: ignore
        assert updated_scenario.updated_by == admin_actor.id  # type: ignore

    async def test_update_scenario_not_found(self, admin_actor: User):
        """
        Test that updating a non-existent financial scenario raises an error.
        """
        repository = ScenarioInMemoryRepository()
        use_case = UpdateScenarioUseCase(repository)
        input_dto = UpdateScenarioInputDTO(
            actor=admin_actor,
            id=uuid4(),
            description="New Description",
            scenario_type=ScenarioType.FORECAST,
        )

        with pytest.raises(ScenarioNotFoundError):
            await use_case.execute(input_dto)

    async def test_update_locked_scenario_fails(self, admin_actor: User):
        """
        Test that updating a locked financial scenario raises an error.
        """
        repository = ScenarioInMemoryRepository()
        scenario = Scenario(
            description="Locked Scenario",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
            is_locked=True,
        )
        await repository.save(scenario)

        use_case = UpdateScenarioUseCase(repository)
        input_dto = UpdateScenarioInputDTO(
            actor=admin_actor,
            id=scenario.id,
            description="New Description",
            scenario_type=ScenarioType.FORECAST,
        )

        with pytest.raises(CannotUpdateLockedScenarioError):
            await use_case.execute(input_dto)

    async def test_update_scenario_with_exchange_rates(self, admin_actor: User):
        """
        Test successful update of a financial scenario with exchange rates.
        """
        repository = ScenarioInMemoryRepository()
        scenario = Scenario(
            description="Scenario to update rates",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
        )
        await repository.save(scenario)

        use_case = UpdateScenarioUseCase(repository)
        exchange_rates = [
            ExchangeRateInputDTO(
                from_currency="GBP",
                to_currency="USD",
                rate=Decimal("1.25"),
                effective_date=date.today(),
            )
        ]

        input_dto = UpdateScenarioInputDTO(
            actor=admin_actor,
            id=scenario.id,
            description="Updated Description",
            scenario_type=ScenarioType.ACTUAL,
            exchange_rates=exchange_rates,
        )

        await use_case.execute(input_dto)

        updated_scenario = await repository.get_by_id(
            scenario.id,
            admin_actor.tenant_id,
        )
        assert updated_scenario.exchange_rates is not None  # type: ignore
        assert len(updated_scenario.exchange_rates) == 1  # type: ignore
        assert str(updated_scenario.exchange_rates[0].from_currency) == "GBP"  # type: ignore
        assert updated_scenario.exchange_rates[0].rate == Decimal("1.25")  # type: ignore
