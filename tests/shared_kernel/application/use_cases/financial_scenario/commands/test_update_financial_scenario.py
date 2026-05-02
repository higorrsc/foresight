from uuid import uuid4

import pytest

from src.identity_access_management.domain.entities import User
from src.shared_kernel.application.use_cases.financial_scenario.commands import (
    UpdateFinancialScenarioInputDTO,
    UpdateFinancialScenarioUseCase,
)
from src.shared_kernel.application.use_cases.financial_scenario.exceptions import (
    CannotUpdateLockedFinancialScenarioError,
    FinancialScenarioNotFoundError,
)
from src.shared_kernel.domain.entities import FinancialScenario, ScenarioType
from tests.fakes.in_memory_repository import FinancialScenarioInMemoryRepository


def test_update_financial_scenario_success(admin_actor: User):
    repository = FinancialScenarioInMemoryRepository()
    scenario = FinancialScenario(
        description="Old Description",
        scenario_type=ScenarioType.ACTUAL,
        tenant_id=admin_actor.tenant_id,
        assumptions=None,
    )
    repository.save(scenario)

    use_case = UpdateFinancialScenarioUseCase(repository)
    input_dto = UpdateFinancialScenarioInputDTO(
        actor=admin_actor,
        id=scenario.id,
        description="New Description",
        scenario_type=ScenarioType.FORECAST,
        is_locked=False,
    )

    result = use_case.execute(input_dto)

    assert result.description == "New Description"
    updated_scenario = repository.get_by_id(scenario.id, admin_actor.tenant_id)
    assert updated_scenario.description == "New Description"  # type: ignore
    assert updated_scenario.scenario_type == ScenarioType.FORECAST  # type: ignore
    assert updated_scenario.updated_by == admin_actor.id  # type: ignore


def test_update_financial_scenario_not_found(admin_actor: User):
    repository = FinancialScenarioInMemoryRepository()
    use_case = UpdateFinancialScenarioUseCase(repository)
    input_dto = UpdateFinancialScenarioInputDTO(
        actor=admin_actor,
        id=uuid4(),
        description="New Description",
        scenario_type=ScenarioType.FORECAST,
    )

    with pytest.raises(FinancialScenarioNotFoundError):
        use_case.execute(input_dto)


def test_update_locked_financial_scenario_fails(admin_actor: User):
    repository = FinancialScenarioInMemoryRepository()
    scenario = FinancialScenario(
        description="Locked Scenario",
        scenario_type=ScenarioType.ACTUAL,
        tenant_id=admin_actor.tenant_id,
        assumptions=None,
        is_locked=True,
    )
    repository.save(scenario)

    use_case = UpdateFinancialScenarioUseCase(repository)
    input_dto = UpdateFinancialScenarioInputDTO(
        actor=admin_actor,
        id=scenario.id,
        description="New Description",
        scenario_type=ScenarioType.FORECAST,
    )

    with pytest.raises(CannotUpdateLockedFinancialScenarioError):
        use_case.execute(input_dto)
