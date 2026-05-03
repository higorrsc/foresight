from uuid import uuid4

import pytest

from src.identity_access_management.domain.entities import User
from src.shared_kernel.application.use_cases.financial_scenario.commands import (
    LockFinancialScenarioInputDTO,
    LockFinancialScenarioUseCase,
)
from src.shared_kernel.domain.entities import FinancialScenario, ScenarioType
from src.shared_kernel.domain.exceptions import (
    FinancialScenarioAlreadyLockedError,
    FinancialScenarioNotFoundError,
)
from tests.fakes.in_memory_repository import FinancialScenarioInMemoryRepository


class TestLockFinancialScenarioUseCase:
    """
    Test suite for the LockFinancialScenarioUseCase.
    """

    def test_lock_financial_scenario_success(self, admin_actor: User):
        """
        Test successful locking of a financial scenario.
        """
        repository = FinancialScenarioInMemoryRepository()
        scenario = FinancialScenario(
            description="To be locked",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
            is_locked=False,
        )
        repository.save(scenario)

        use_case = LockFinancialScenarioUseCase(repository)
        input_dto = LockFinancialScenarioInputDTO(actor=admin_actor, id=scenario.id)

        use_case.execute(input_dto)

        locked_scenario = repository.get_by_id(scenario.id, admin_actor.tenant_id)
        assert locked_scenario.is_locked is True  # type: ignore
        assert locked_scenario.updated_by == admin_actor.id  # type: ignore

    def test_lock_financial_scenario_already_locked(self, admin_actor: User):
        """
        Test that locking an already locked financial scenario raises an error.
        """
        repository = FinancialScenarioInMemoryRepository()
        scenario = FinancialScenario(
            description="Already locked",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
            is_locked=True,
        )
        repository.save(scenario)

        use_case = LockFinancialScenarioUseCase(repository)
        input_dto = LockFinancialScenarioInputDTO(actor=admin_actor, id=scenario.id)

        with pytest.raises(FinancialScenarioAlreadyLockedError):
            use_case.execute(input_dto)

    def test_lock_financial_scenario_not_found(self, admin_actor: User):
        """
        Test that locking a non-existent financial scenario raises an error.
        """
        repository = FinancialScenarioInMemoryRepository()
        use_case = LockFinancialScenarioUseCase(repository)
        input_dto = LockFinancialScenarioInputDTO(actor=admin_actor, id=uuid4())

        with pytest.raises(FinancialScenarioNotFoundError):
            use_case.execute(input_dto)
