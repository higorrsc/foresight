from uuid import uuid4

import pytest

from src.identity_access_management.domain.entities import User
from src.planning.application.use_cases.scenario.commands import (
    UpdateScenarioInputDTO,
    UpdateScenarioUseCase,
)
from src.planning.domain.entities import Scenario, ScenarioType
from src.planning.domain.exceptions import (
    CannotUpdateLockedScenarioError,
    ScenarioNotFoundError,
)
from tests.fakes import ScenarioInMemoryRepository


class TestUpdateScenarioUseCase:
    """
    Test suite for the UpdateScenarioUseCase.
    """

    def test_update_financial_scenario_success(self, admin_actor: User):
        """
        Test successful update of a financial scenario.
        """
        repository = ScenarioInMemoryRepository()
        scenario = Scenario(
            description="Old Description",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
        )
        repository.save(scenario)

        use_case = UpdateScenarioUseCase(repository)
        input_dto = UpdateScenarioInputDTO(
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

    def test_update_financial_scenario_not_found(self, admin_actor: User):
        """
        Test that updating a non-existent financial scenario raises an error.
        """
        repository = ScenarioInMemoryRepository()
        use_case = UpdateScenarioUseCase(repository)
        input_dto = UpdateScenarioInputDTO(
            actor=admin_actor,
            id=uuid4(),
            description="New Description",
            scenario_type=ScenarioType.FORECAST,
        )

        with pytest.raises(ScenarioNotFoundError):
            use_case.execute(input_dto)

    def test_update_locked_financial_scenario_fails(self, admin_actor: User):
        """
        Test that updating a locked financial scenario raises an error.
        """
        repository = ScenarioInMemoryRepository()
        scenario = Scenario(
            description="Locked Scenario",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
            is_locked=True,
        )
        repository.save(scenario)

        use_case = UpdateScenarioUseCase(repository)
        input_dto = UpdateScenarioInputDTO(
            actor=admin_actor,
            id=scenario.id,
            description="New Description",
            scenario_type=ScenarioType.FORECAST,
        )

        with pytest.raises(CannotUpdateLockedScenarioError):
            use_case.execute(input_dto)
