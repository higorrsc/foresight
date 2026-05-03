from uuid import uuid4

import pytest

from src.core.application.use_cases.queries import GetByIdRequestInputDTO
from src.identity_access_management.domain.entities import User
from src.planning.application.use_cases.scenario.queries import (
    GetScenarioByIdUseCase,
)
from src.planning.domain.entities import Scenario, ScenarioType
from src.planning.domain.exceptions import (
    ScenarioNotFoundError,
)
from tests.fakes import ScenarioInMemoryRepository


class TestGetScenarioByIdUseCase:
    """
    Test suite for the GetScenarioByIdUseCase.
    """

    def test_get_financial_scenario_by_id_success(self, admin_actor: User):
        """
        Test successful retrieval of a financial scenario by its ID.
        """
        repository = ScenarioInMemoryRepository()
        scenario = Scenario(
            description="Found me",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
        )
        repository.save(scenario)

        use_case = GetScenarioByIdUseCase(repository)
        input_dto = GetByIdRequestInputDTO(actor=admin_actor, id=scenario.id)

        result = use_case.execute(input_dto)

        assert result.id == scenario.id
        assert result.description == "Found me"

    def test_get_financial_scenario_by_id_not_found(self, admin_actor: User):
        """
        Test that retrieving a non-existent financial scenario raises an error.
        """
        repository = ScenarioInMemoryRepository()
        use_case = GetScenarioByIdUseCase(repository)
        input_dto = GetByIdRequestInputDTO(actor=admin_actor, id=uuid4())

        with pytest.raises(ScenarioNotFoundError):
            use_case.execute(input_dto)
