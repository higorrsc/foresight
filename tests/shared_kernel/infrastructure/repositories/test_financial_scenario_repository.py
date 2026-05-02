from sqlalchemy.orm import Session

from src.shared_kernel.domain.entities import FinancialScenario, ScenarioType
from src.shared_kernel.infrastructure.repositories import FinancialScenarioRepository
from src.tenant_management.infrastructure.models import TenantModel


def test_financial_scenario_repository_save_and_get_by_id(
    db_session_for_test: Session,
    default_tenant: TenantModel,
):
    repository = FinancialScenarioRepository(db_session_for_test)
    scenario = FinancialScenario(
        description="Test Scenario",
        scenario_type=ScenarioType.ACTUAL,
        tenant_id=default_tenant.id,  # type: ignore
        assumptions=None,
    )

    repository.save(scenario)

    saved_scenario = repository.get_by_id(scenario.id, default_tenant.id)  # type: ignore

    assert saved_scenario is not None
    assert saved_scenario.id == scenario.id
    assert saved_scenario.description == "Test Scenario"
    assert saved_scenario.scenario_type == ScenarioType.ACTUAL
    assert saved_scenario.tenant_id == default_tenant.id


def test_financial_scenario_repository_update(
    db_session_for_test: Session,
    default_tenant: TenantModel,
):
    repository = FinancialScenarioRepository(db_session_for_test)
    scenario = FinancialScenario(
        description="Original Description",
        scenario_type=ScenarioType.ACTUAL,
        tenant_id=default_tenant.id,  # type: ignore
        assumptions=None,
    )
    repository.save(scenario)

    scenario.description = "Updated Description"
    repository.update(scenario)

    updated_scenario = repository.get_by_id(scenario.id, default_tenant.id)  # type: ignore
    assert updated_scenario.description == "Updated Description"  # type: ignore


def test_financial_scenario_repository_delete(
    db_session_for_test: Session,
    default_tenant: TenantModel,
):
    repository = FinancialScenarioRepository(db_session_for_test)
    scenario = FinancialScenario(
        description="To be deleted",
        scenario_type=ScenarioType.ACTUAL,
        tenant_id=default_tenant.id,  # type: ignore
        assumptions=None,
    )
    repository.save(scenario)

    repository.delete(scenario.id, default_tenant.id)  # type: ignore

    deleted_scenario = repository.get_by_id(scenario.id, default_tenant.id)  # type: ignore
    assert deleted_scenario is None


def test_financial_scenario_repository_list(
    db_session_for_test: Session,
    default_tenant: TenantModel,
):
    repository = FinancialScenarioRepository(db_session_for_test)
    scenario1 = FinancialScenario(
        description="Scenario 1",
        scenario_type=ScenarioType.ACTUAL,
        tenant_id=default_tenant.id,  # type: ignore
        assumptions=None,
    )
    scenario2 = FinancialScenario(
        description="Scenario 2",
        scenario_type=ScenarioType.BUDGET,
        tenant_id=default_tenant.id,  # type: ignore
        assumptions=None,
    )
    repository.save(scenario1)
    repository.save(scenario2)

    result = repository.search(tenant_id=default_tenant.id)  # type: ignore

    assert result.total == 2
    assert len(result.data) == 2
