from src.identity_access_management.domain.entities import User
from src.planning.application.use_cases.scenario.commands import (
    CreateScenarioInputDTO,
    CreateScenarioUseCase,
)
from src.planning.domain.entities import ScenarioType
from tests.fakes import ScenarioInMemoryRepository


class TestCreateScenarioUseCase:
    """
    Test suite for the CreateScenarioUseCase.
    """

    def test_create_financial_scenario_success(self, admin_actor: User):
        """
        Test successful creation of a financial scenario.
        """
        repository = ScenarioInMemoryRepository()
        use_case = CreateScenarioUseCase(repository)

        input_dto = CreateScenarioInputDTO(
            actor=admin_actor,
            description="New Scenario",
            scenario_type=ScenarioType.BUDGET,
            assumptions="Some assumptions",
        )

        result = use_case.execute(input_dto)

        assert result.id is not None
        saved_scenario = repository.get_by_id(result.id, admin_actor.tenant_id)
        assert saved_scenario.description == "New Scenario"  # type: ignore
        assert saved_scenario.scenario_type == ScenarioType.BUDGET  # type: ignore
        assert saved_scenario.assumptions == "Some assumptions"  # type: ignore
        assert saved_scenario.tenant_id == admin_actor.tenant_id  # type: ignore
        assert saved_scenario.created_by == admin_actor.id  # type: ignore
