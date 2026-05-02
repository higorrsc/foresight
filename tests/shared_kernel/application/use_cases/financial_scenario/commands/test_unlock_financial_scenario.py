from uuid import uuid4

import pytest

from src.identity_access_management.domain.entities import User
from src.shared_kernel.application.use_cases.financial_scenario.commands import (
    UnlockFinancialScenarioInputDTO,
    UnlockFinancialScenarioUseCase,
)
from src.shared_kernel.application.use_cases.financial_scenario.exceptions import (
    FinancialScenarioAlreadyUnlockedError,
    FinancialScenarioNotFoundError,
)
from src.shared_kernel.domain.entities import FinancialScenario, ScenarioType
from tests.fakes.in_memory_repository import FinancialScenarioInMemoryRepository


class TestUnlockFinancialScenarioUseCase:
    """
    Test suite for the UnlockFinancialScenarioUseCase.
    """

    def test_unlock_financial_scenario_success(self, admin_actor: User):
        """
        Test successful unlocking of a financial scenario.
        """
        repository = FinancialScenarioInMemoryRepository()
        scenario = FinancialScenario(
            description="To be unlocked",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
            is_locked=True,
        )
        repository.save(scenario)

        use_case = UnlockFinancialScenarioUseCase(repository)
        input_dto = UnlockFinancialScenarioInputDTO(actor=admin_actor, id=scenario.id)

        use_case.execute(input_dto)

        unlocked_scenario = repository.get_by_id(scenario.id, admin_actor.tenant_id)
        assert unlocked_scenario.is_locked is False  # type: ignore
        assert unlocked_scenario.updated_by == admin_actor.id  # type: ignore

    def test_unlock_financial_scenario_already_unlocked(self, admin_actor: User):
        """
        Test that unlocking an already unlocked financial scenario raises an error.
        """
        repository = FinancialScenarioInMemoryRepository()
        scenario = FinancialScenario(
            description="Already unlocked",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
            is_locked=False,
        )
        repository.save(scenario)

        use_case = UnlockFinancialScenarioUseCase(repository)
        input_dto = UnlockFinancialScenarioInputDTO(actor=admin_actor, id=scenario.id)

        with pytest.raises(FinancialScenarioAlreadyUnlockedError):
            use_case.execute(input_dto)

    def test_unlock_financial_scenario_not_found(self, admin_actor: User):
        """
        Test that unlocking a non-existent financial scenario raises an error.
        """
        repository = FinancialScenarioInMemoryRepository()
        use_case = UnlockFinancialScenarioUseCase(repository)
        input_dto = UnlockFinancialScenarioInputDTO(actor=admin_actor, id=uuid4())

        with pytest.raises(FinancialScenarioNotFoundError):
            use_case.execute(input_dto)
