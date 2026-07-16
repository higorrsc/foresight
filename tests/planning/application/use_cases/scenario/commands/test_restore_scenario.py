from uuid import uuid4

import pytest

from src.core.application.use_cases.commands.generic_restore import (
    RestoreRequestInputDTO,
)
from src.identity_access_management.domain.entities import User
from src.planning.application.use_cases.scenario.commands import (
    RestoreScenarioUseCase,
)
from src.planning.domain.entities import Scenario, ScenarioType
from src.planning.domain.exceptions import ScenarioNotFoundError
from tests.fakes import ScenarioInMemoryRepository


class TestRestoreScenarioUseCase:
    """
    Test suite for the RestoreScenarioUseCase.
    """

    async def test_restore_scenario_success(self, admin_actor: User):
        """
        Test successful restoration of a soft-deleted financial scenario.
        """
        repository = ScenarioInMemoryRepository()
        scenario = Scenario(
            description="To be restored",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
        )
        scenario.soft_delete()
        await repository.save(scenario)

        use_case = RestoreScenarioUseCase(repository)
        input_dto = RestoreRequestInputDTO(actor=admin_actor, id=scenario.id)

        await use_case.execute(input_dto)

        restored_scenario = await repository.get_by_id(
            scenario.id,
            admin_actor.tenant_id,
        )
        assert restored_scenario is not None
        assert restored_scenario.is_active is True

    async def test_restore_scenario_not_found(self, admin_actor: User):
        """
        Test that restoring a non-existent financial scenario raises an error.
        """
        repository = ScenarioInMemoryRepository()
        use_case = RestoreScenarioUseCase(repository)
        input_dto = RestoreRequestInputDTO(actor=admin_actor, id=uuid4())

        with pytest.raises(ScenarioNotFoundError):
            await use_case.execute(input_dto)
