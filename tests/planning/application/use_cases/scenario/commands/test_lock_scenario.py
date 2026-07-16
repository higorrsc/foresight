from uuid import uuid4

import pytest

from src.identity_access_management.domain.entities import User
from src.planning.application.use_cases.scenario.commands import (
    LockScenarioInputDTO,
    LockScenarioUseCase,
)
from src.planning.domain.entities import Scenario, ScenarioType
from src.planning.domain.exceptions import (
    ScenarioAlreadyLockedError,
    ScenarioNotFoundError,
)
from tests.fakes import ScenarioInMemoryRepository


class TestLockScenarioUseCase:
    """
    Test suite for the LockScenarioUseCase.
    """

    async def test_lock_scenario_success(self, guest_actor: User):
        """
        Test successful locking of a financial scenario.
        """
        repository = ScenarioInMemoryRepository()
        scenario = Scenario(
            description="To be locked",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=guest_actor.tenant_id,
            assumptions=None,
            is_locked=False,
        )
        await repository.save(scenario)

        use_case = LockScenarioUseCase(repository)
        input_dto = LockScenarioInputDTO(actor=guest_actor, id=scenario.id)

        await use_case.execute(input_dto)

        locked_scenario = await repository.get_by_id(scenario.id, guest_actor.tenant_id)
        assert locked_scenario.is_locked is True  # type: ignore
        assert locked_scenario.updated_by == guest_actor.id  # type: ignore

    async def test_lock_scenario_already_locked(self, guest_actor: User):
        """
        Test that locking an already locked financial scenario raises an error.
        """
        repository = ScenarioInMemoryRepository()
        scenario = Scenario(
            description="Already locked",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=guest_actor.tenant_id,
            assumptions=None,
            is_locked=True,
        )
        await repository.save(scenario)

        use_case = LockScenarioUseCase(repository)
        input_dto = LockScenarioInputDTO(actor=guest_actor, id=scenario.id)

        with pytest.raises(ScenarioAlreadyLockedError):
            await use_case.execute(input_dto)

    async def test_lock_scenario_not_found(self, guest_actor: User):
        """
        Test that locking a non-existent financial scenario raises an error.
        """
        repository = ScenarioInMemoryRepository()
        use_case = LockScenarioUseCase(repository)
        input_dto = LockScenarioInputDTO(actor=guest_actor, id=uuid4())

        with pytest.raises(ScenarioNotFoundError):
            await use_case.execute(input_dto)
