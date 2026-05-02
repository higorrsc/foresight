from src.core.application.use_cases.queries import ListRequestInputDTO
from src.identity_access_management.domain.entities import User
from src.shared_kernel.application.use_cases.financial_scenario.queries import (
    ListFinancialScenarioUseCase,
)
from src.shared_kernel.domain.entities import FinancialScenario, ScenarioType
from tests.fakes.in_memory_repository import FinancialScenarioInMemoryRepository


def test_list_financial_scenarios_success(admin_actor: User):
    repository = FinancialScenarioInMemoryRepository()
    scenario1 = FinancialScenario(
        description="Scenario A",
        scenario_type=ScenarioType.ACTUAL,
        tenant_id=admin_actor.tenant_id,
        assumptions=None,
    )
    scenario2 = FinancialScenario(
        description="Scenario B",
        scenario_type=ScenarioType.BUDGET,
        tenant_id=admin_actor.tenant_id,
        assumptions=None,
    )
    repository.save(scenario1)
    repository.save(scenario2)

    use_case = ListFinancialScenarioUseCase(repository)
    input_dto = ListRequestInputDTO(actor=admin_actor)

    result = use_case.execute(input_dto)

    assert result.meta.total_items == 2
    assert len(result.data) == 2
    assert result.data[0].description == "Scenario A"
    assert result.data[1].description == "Scenario B"


def test_list_financial_scenarios_filter_by_description(admin_actor: User):
    repository = FinancialScenarioInMemoryRepository()
    scenario1 = FinancialScenario(
        description="Target",
        scenario_type=ScenarioType.ACTUAL,
        tenant_id=admin_actor.tenant_id,
        assumptions=None,
    )
    scenario2 = FinancialScenario(
        description="Other",
        scenario_type=ScenarioType.BUDGET,
        tenant_id=admin_actor.tenant_id,
        assumptions=None,
    )
    repository.save(scenario1)
    repository.save(scenario2)

    use_case = ListFinancialScenarioUseCase(repository)
    input_dto = ListRequestInputDTO(
        actor=admin_actor, filters={"description": "Target"}
    )

    result = use_case.execute(input_dto)

    assert result.meta.total_items == 1
    assert len(result.data) == 1
    assert result.data[0].description == "Target"
