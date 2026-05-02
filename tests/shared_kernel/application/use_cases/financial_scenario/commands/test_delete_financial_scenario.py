from uuid import uuid4

import pytest

from src.core.application.use_cases.commands.generic_delete import DeleteRequestInputDTO
from src.identity_access_management.domain.entities import User
from src.shared_kernel.application.use_cases.financial_scenario.commands import (
    DeleteFinancialScenarioUseCase,
)
from src.shared_kernel.application.use_cases.financial_scenario.exceptions import (
    FinancialScenarioNotFoundError,
)
from src.shared_kernel.domain.entities import FinancialScenario, ScenarioType
from tests.fakes.in_memory_repository import FinancialScenarioInMemoryRepository


def test_delete_financial_scenario_success(admin_actor: User):
    repository = FinancialScenarioInMemoryRepository()
    scenario = FinancialScenario(
        description="To be deleted",
        scenario_type=ScenarioType.ACTUAL,
        tenant_id=admin_actor.tenant_id,
        assumptions=None,
    )
    repository.save(scenario)

    use_case = DeleteFinancialScenarioUseCase(repository)
    input_dto = DeleteRequestInputDTO(actor=admin_actor, id=scenario.id)

    use_case.execute(input_dto)

    deleted_scenario = repository.get_by_id(scenario.id, admin_actor.tenant_id)
    assert deleted_scenario is not None
    assert deleted_scenario.is_active is False


def test_delete_financial_scenario_not_found(admin_actor: User):
    repository = FinancialScenarioInMemoryRepository()
    use_case = DeleteFinancialScenarioUseCase(repository)
    input_dto = DeleteRequestInputDTO(actor=admin_actor, id=uuid4())

    with pytest.raises(FinancialScenarioNotFoundError):
        use_case.execute(input_dto)
