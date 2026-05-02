from uuid import uuid4

import pytest

from src.core.application.use_cases.queries import GetByIdRequestInputDTO
from src.identity_access_management.domain.entities import User
from src.shared_kernel.application.use_cases.financial_scenario.exceptions import (
    FinancialScenarioNotFoundError,
)
from src.shared_kernel.application.use_cases.financial_scenario.queries import (
    GetFinancialScenarioByIdUseCase,
)
from src.shared_kernel.domain.entities import FinancialScenario, ScenarioType
from tests.fakes.in_memory_repository import FinancialScenarioInMemoryRepository


def test_get_financial_scenario_by_id_success(admin_actor: User):
    repository = FinancialScenarioInMemoryRepository()
    scenario = FinancialScenario(
        description="Found me",
        scenario_type=ScenarioType.ACTUAL,
        tenant_id=admin_actor.tenant_id,
        assumptions=None,
    )
    repository.save(scenario)

    use_case = GetFinancialScenarioByIdUseCase(repository)
    input_dto = GetByIdRequestInputDTO(actor=admin_actor, id=scenario.id)

    result = use_case.execute(input_dto)

    assert result.id == scenario.id
    assert result.description == "Found me"


def test_get_financial_scenario_by_id_not_found(admin_actor: User):
    repository = FinancialScenarioInMemoryRepository()
    use_case = GetFinancialScenarioByIdUseCase(repository)
    input_dto = GetByIdRequestInputDTO(actor=admin_actor, id=uuid4())

    with pytest.raises(FinancialScenarioNotFoundError):
        use_case.execute(input_dto)
