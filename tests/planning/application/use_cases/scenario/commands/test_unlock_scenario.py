from uuid import uuid4

import pytest

from src.identity_access_management.domain.entities import User
from src.planning.application.use_cases.scenario.commands import (
    UnlockScenarioInputDTO,
    UnlockScenarioUseCase,
)
from src.planning.domain.entities import Scenario, ScenarioType
from src.planning.domain.exceptions import (
    ScenarioAlreadyUnlockedError,
    ScenarioNotFoundError,
)
from tests.fakes import ScenarioInMemoryRepository


class TestUnlockScenarioUseCase:
    """
    Test suite for the UnlockScenarioUseCase.
    """

    def test_unlock_scenario_success(self, admin_actor: User):
        """
        Test successful unlocking of a financial scenario.
        """
        repository = ScenarioInMemoryRepository()
        scenario = Scenario(
            description="To be unlocked",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
            is_locked=True,
        )
        repository.save(scenario)

        use_case = UnlockScenarioUseCase(repository)
        input_dto = UnlockScenarioInputDTO(actor=admin_actor, id=scenario.id)

        use_case.execute(input_dto)

        unlocked_scenario = repository.get_by_id(scenario.id, admin_actor.tenant_id)
        assert unlocked_scenario.is_locked is False  # type: ignore
        assert unlocked_scenario.updated_by == admin_actor.id  # type: ignore

    def test_unlock_scenario_already_unlocked(self, admin_actor: User):
        """
        Test that unlocking an already unlocked financial scenario raises an error.
        """
        repository = ScenarioInMemoryRepository()
        scenario = Scenario(
            description="Already unlocked",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
            is_locked=False,
        )
        repository.save(scenario)

        use_case = UnlockScenarioUseCase(repository)
        input_dto = UnlockScenarioInputDTO(actor=admin_actor, id=scenario.id)

        with pytest.raises(ScenarioAlreadyUnlockedError):
            use_case.execute(input_dto)

    def test_unlock_scenario_not_found(self, admin_actor: User):
        """
        Test that unlocking a non-existent financial scenario raises an error.
        """
        repository = ScenarioInMemoryRepository()
        use_case = UnlockScenarioUseCase(repository)
        input_dto = UnlockScenarioInputDTO(actor=admin_actor, id=uuid4())

        with pytest.raises(ScenarioNotFoundError):
            use_case.execute(input_dto)
