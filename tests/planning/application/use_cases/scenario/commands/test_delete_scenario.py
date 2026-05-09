from uuid import uuid4

import pytest

from src.core.application.use_cases.commands.generic_delete import DeleteRequestInputDTO
from src.identity_access_management.domain.entities import User
from src.planning.application.use_cases.scenario.commands import (
    DeleteScenarioUseCase,
)
from src.planning.domain.entities import Scenario, ScenarioType
from src.planning.domain.exceptions import ScenarioNotFoundError
from tests.fakes import ScenarioInMemoryRepository


class TestDeleteScenarioUseCase:
    """
    Test suite for the DeleteScenarioUseCase.
    """

    async def test_delete_scenario_success(self, admin_actor: User):
        """
        Test successful deletion (soft delete) of a financial scenario.
        """
        repository = ScenarioInMemoryRepository()
        scenario = Scenario(
            description="To be deleted",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
        )
        await repository.save(scenario)

        use_case = DeleteScenarioUseCase(repository)
        input_dto = DeleteRequestInputDTO(actor=admin_actor, id=scenario.id)

        await use_case.execute(input_dto)

        deleted_scenario = await repository.get_by_id(
            scenario.id,
            admin_actor.tenant_id,
        )
        assert deleted_scenario is not None
        assert deleted_scenario.is_active is False

    async def test_delete_scenario_not_found(self, admin_actor: User):
        """
        Test that deleting a non-existent financial scenario raises an error.
        """
        repository = ScenarioInMemoryRepository()
        use_case = DeleteScenarioUseCase(repository)
        input_dto = DeleteRequestInputDTO(actor=admin_actor, id=uuid4())

        with pytest.raises(ScenarioNotFoundError):
            await use_case.execute(input_dto)
