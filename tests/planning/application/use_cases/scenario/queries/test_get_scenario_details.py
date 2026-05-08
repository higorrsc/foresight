from uuid import uuid4

import pytest

from src.core.application.use_cases.queries import GetByIdRequestInputDTO
from src.identity_access_management.domain.entities import User
from src.planning.application.use_cases.scenario.queries import (
    GetScenarioDetailsUseCase,
)
from src.planning.domain.entities import Scenario, ScenarioType
from src.planning.domain.exceptions import ScenarioNotFoundError
from tests.fakes import ScenarioInMemoryRepository


class TestGetScenarioDetailsUseCase:
    """
    Test suite for the GetScenarioDetailsUseCase.
    """

    def test_get_scenario_details_success(self, admin_actor: User):
        """
        Test successful retrieval of scenario details.
        """
        repository = ScenarioInMemoryRepository()
        use_case = GetScenarioDetailsUseCase(repository)

        scenario = Scenario(
            description="Test Scenario",
            scenario_type=ScenarioType.BUDGET,
            assumptions="Some assumptions",
            tenant_id=admin_actor.tenant_id,
        )
        repository.save(scenario)

        input_dto = GetByIdRequestInputDTO(
            actor=admin_actor,
            id=scenario.id,
        )

        result = use_case.execute(input_dto)

        assert result.id == scenario.id
        assert result.description == "Test Scenario"

    def test_get_scenario_details_not_found(self, admin_actor: User):
        """
        Test error when scenario is not found.
        """
        repository = ScenarioInMemoryRepository()
        use_case = GetScenarioDetailsUseCase(repository)

        input_dto = GetByIdRequestInputDTO(
            actor=admin_actor,
            id=uuid4(),
        )

        with pytest.raises(ScenarioNotFoundError):
            use_case.execute(input_dto)
