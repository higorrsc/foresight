from decimal import Decimal

from src.identity_access_management.domain.entities import User
from src.planning.application.use_cases.scenario.commands import (
    CreateScenarioInputDTO,
    CreateScenarioUseCase,
    ExchangeRateInputDTO,
)
from src.planning.domain.entities import ScenarioType
from tests.fakes import ScenarioInMemoryRepository


class TestCreateScenarioUseCase:
    """
    Test suite for the CreateScenarioUseCase.
    """

    def test_create_financial_scenario_success(self, admin_actor: User):
        """
        Test successful creation of a financial scenario.
        """
        repository = ScenarioInMemoryRepository()
        use_case = CreateScenarioUseCase(repository)

        input_dto = CreateScenarioInputDTO(
            actor=admin_actor,
            description="New Scenario",
            scenario_type=ScenarioType.BUDGET,
            assumptions="Some assumptions",
        )

        result = use_case.execute(input_dto)

        assert result.id is not None
        saved_scenario = repository.get_by_id(result.id, admin_actor.tenant_id)
        assert saved_scenario.description == "New Scenario"  # type: ignore
        assert saved_scenario.scenario_type == ScenarioType.BUDGET  # type: ignore
        assert saved_scenario.assumptions == "Some assumptions"  # type: ignore
        assert saved_scenario.tenant_id == admin_actor.tenant_id  # type: ignore
        assert saved_scenario.created_by == admin_actor.id  # type: ignore

    def test_create_financial_scenario_with_exchange_rates(self, admin_actor: User):
        """
        Test successful creation of a financial scenario with exchange rates.
        """
        repository = ScenarioInMemoryRepository()
        use_case = CreateScenarioUseCase(repository)

        exchange_rates = [
            ExchangeRateInputDTO(
                from_currency="USD",
                to_currency="BRL",
                rate=Decimal("5.0"),
            )
        ]

        input_dto = CreateScenarioInputDTO(
            actor=admin_actor,
            description="Scenario with Rates",
            scenario_type=ScenarioType.ACTUAL,
            exchange_rates=exchange_rates,
        )

        result = use_case.execute(input_dto)

        saved_scenario = repository.get_by_id(result.id, admin_actor.tenant_id)
        assert saved_scenario.exchange_rates is not None  # type: ignore
        assert len(saved_scenario.exchange_rates) == 1  # type: ignore
        assert str(saved_scenario.exchange_rates[0].from_currency) == "USD"  # type: ignore
        assert saved_scenario.exchange_rates[0].rate == Decimal("5.0")  # type: ignore
        assert saved_scenario.exchange_rates[0].scenario_id == result.id  # type: ignore
