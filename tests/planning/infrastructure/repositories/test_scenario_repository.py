from datetime import date
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from src.finance.domain.value_objects import CurrencyCode
from src.planning.domain.entities import ExchangeRate, Scenario, ScenarioType
from src.planning.infrastructure.repositories import (
    ExchangeRateRepository,
    ScenarioRepository,
)
from src.tenant_management.infrastructure.models import TenantModel


class TestScenarioRepository:
    """
    Test suite for the ScenarioRepository.
    """

    async def test_scenario_repository_save_and_get_by_id(
        self,
        db_session_for_test: AsyncSession,
        default_tenant: TenantModel,
    ):
        """
        Test saving a financial scenario and retrieving it by its ID.
        """
        repository = ScenarioRepository(db_session_for_test)
        scenario = Scenario(
            description="Test Scenario",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=default_tenant.id,  # type: ignore
            assumptions=None,
        )

        await repository.save(scenario)

        saved_scenario = await repository.get_by_id(scenario.id, default_tenant.id)  # type: ignore

        assert saved_scenario is not None
        assert saved_scenario.id == scenario.id
        assert saved_scenario.description == "Test Scenario"
        assert saved_scenario.scenario_type == ScenarioType.ACTUAL
        assert saved_scenario.tenant_id == default_tenant.id

    async def test_scenario_repository_update(
        self,
        db_session_for_test: AsyncSession,
        default_tenant: TenantModel,
    ):
        """
        Test updating an existing financial scenario.
        """

        repository = ScenarioRepository(db_session_for_test)
        scenario = Scenario(
            description="Original Description",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=default_tenant.id,  # type: ignore
            assumptions=None,
        )
        await repository.save(scenario)

        scenario.description = "Updated Description"
        await repository.update(scenario)

        updated_scenario = await repository.get_by_id(
            scenario.id,
            default_tenant.id,  # type: ignore
        )  # type: ignore
        assert updated_scenario.description == "Updated Description"  # type: ignore

    async def test_scenario_repository_delete(
        self,
        db_session_for_test: AsyncSession,
        default_tenant: TenantModel,
    ):
        """
        Test deleting a financial scenario.
        """
        repository = ScenarioRepository(db_session_for_test)
        scenario = Scenario(
            description="To be deleted",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=default_tenant.id,  # type: ignore
            assumptions=None,
        )
        await repository.save(scenario)

        await repository.delete(scenario.id, default_tenant.id)  # type: ignore

        deleted_scenario = await repository.get_by_id(
            scenario.id,
            default_tenant.id,  # type: ignore
        )
        assert deleted_scenario is None

    async def test_scenario_repository_list(
        self,
        db_session_for_test: AsyncSession,
        default_tenant: TenantModel,
    ):
        """
        Test searching and listing financial scenarios.
        """
        repository = ScenarioRepository(db_session_for_test)
        scenario1 = Scenario(
            description="Scenario 1",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=default_tenant.id,  # type: ignore
            assumptions=None,
        )
        scenario2 = Scenario(
            description="Scenario 2",
            scenario_type=ScenarioType.BUDGET,
            tenant_id=default_tenant.id,  # type: ignore
            assumptions=None,
        )
        await repository.save(scenario1)
        await repository.save(scenario2)

        result = await repository.search(tenant_id=default_tenant.id)  # type: ignore

        assert result.total == 2
        assert len(result.data) == 2

    async def test_scenario_repository_with_exchange_rates(
        self,
        db_session_for_test: AsyncSession,
        default_tenant: TenantModel,
    ):
        """
        Test saving a scenario with exchange rates.
        """
        repository = ScenarioRepository(db_session_for_test)
        scenario = Scenario(
            description="Scenario with rates",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=default_tenant.id,  # type: ignore
            assumptions=None,
        )
        rate = ExchangeRate(
            scenario_id=scenario.id,
            from_currency=CurrencyCode(value="USD"),
            to_currency=CurrencyCode(value="BRL"),
            rate=Decimal("5.0"),
            effective_date=date.today(),
        )
        scenario.exchange_rates = [rate]

        await repository.save(scenario)

        saved = await repository.get_by_id(scenario.id, default_tenant.id)  # type: ignore
        assert saved is not None
        assert saved.exchange_rates is not None
        assert len(saved.exchange_rates) == 1
        assert str(saved.exchange_rates[0].from_currency) == "USD"
        assert saved.exchange_rates[0].rate == Decimal("5.0")

    async def test_exchange_rate_repository(
        self,
        db_session_for_test: AsyncSession,
        default_tenant: TenantModel,
    ):
        """
        Test the ExchangeRateRepository directly.
        """
        scenario_repo = ScenarioRepository(db_session_for_test)
        scenario = Scenario(
            description="Parent Scenario",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=default_tenant.id,  # type: ignore
            assumptions=None,
        )
        await scenario_repo.save(scenario)

        er_repo = ExchangeRateRepository(db_session_for_test)
        rate = ExchangeRate(
            scenario_id=scenario.id,
            from_currency=CurrencyCode(value="EUR"),
            to_currency=CurrencyCode(value="USD"),
            rate=Decimal("1.1"),
            effective_date=date.today(),
        )
        await er_repo.save(rate)

        saved_rate = await er_repo.get_by_id(rate.id, None)
        assert saved_rate is not None
        assert saved_rate.rate == Decimal("1.1")
        assert saved_rate.scenario_id == scenario.id
