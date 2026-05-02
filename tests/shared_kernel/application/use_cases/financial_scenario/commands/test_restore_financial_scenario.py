from uuid import uuid4

import pytest

from src.core.application.use_cases.commands.generic_restore import (
    RestoreRequestInputDTO,
)
from src.identity_access_management.domain.entities import User
from src.shared_kernel.application.use_cases.financial_scenario.commands import (
    RestoreFinancialScenarioUseCase,
)
from src.shared_kernel.application.use_cases.financial_scenario.exceptions import (
    FinancialScenarioNotFoundError,
)
from src.shared_kernel.domain.entities import FinancialScenario, ScenarioType
from tests.fakes.in_memory_repository import FinancialScenarioInMemoryRepository


class TestRestoreFinancialScenarioUseCase:
    """
    Test suite for the RestoreFinancialScenarioUseCase.
    """

    def test_restore_financial_scenario_success(self, admin_actor: User):
        """
        Test successful restoration of a soft-deleted financial scenario.
        """
        repository = FinancialScenarioInMemoryRepository()
        scenario = FinancialScenario(
            description="To be restored",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
        )
        scenario.soft_delete()
        repository.save(scenario)

        use_case = RestoreFinancialScenarioUseCase(repository)
        input_dto = RestoreRequestInputDTO(actor=admin_actor, id=scenario.id)

        use_case.execute(input_dto)

        restored_scenario = repository.get_by_id(scenario.id, admin_actor.tenant_id)
        assert restored_scenario is not None
        assert restored_scenario.is_active is True

    def test_restore_financial_scenario_not_found(self, admin_actor: User):
        """
        Test that restoring a non-existent financial scenario raises an error.
        """
        repository = FinancialScenarioInMemoryRepository()
        use_case = RestoreFinancialScenarioUseCase(repository)
        input_dto = RestoreRequestInputDTO(actor=admin_actor, id=uuid4())

        with pytest.raises(FinancialScenarioNotFoundError):
            use_case.execute(input_dto)
