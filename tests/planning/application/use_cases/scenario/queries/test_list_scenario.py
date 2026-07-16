from src.core.application.use_cases.queries import ListRequestInputDTO
from src.identity_access_management.domain.entities import User
from src.planning.application.use_cases.scenario.queries import (
    ListScenarioUseCase,
)
from src.planning.domain.entities import Scenario, ScenarioType
from tests.fakes import ScenarioInMemoryRepository


class TestListScenarioUseCase:
    """
    Test suite for the ListScenarioUseCase.
    """

    async def test_list_financial_scenarios_success(self, admin_actor: User):
        """
        Test successful listing of financial scenarios.
        """
        repository = ScenarioInMemoryRepository()
        scenario1 = Scenario(
            description="Scenario A",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
        )
        scenario2 = Scenario(
            description="Scenario B",
            scenario_type=ScenarioType.BUDGET,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
        )
        await repository.save(scenario1)
        await repository.save(scenario2)

        use_case = ListScenarioUseCase(repository)
        input_dto = ListRequestInputDTO(actor=admin_actor)

        result = await use_case.execute(input_dto)

        assert result.meta.total_items == 2
        assert len(result.data) == 2
        assert result.data[0].description == "Scenario A"
        assert result.data[1].description == "Scenario B"

    async def test_list_financial_scenarios_filter_by_description(
        self, admin_actor: User
    ):
        """
        Test listing financial scenarios with a description filter.
        """
        repository = ScenarioInMemoryRepository()
        scenario1 = Scenario(
            description="Target",
            scenario_type=ScenarioType.ACTUAL,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
        )
        scenario2 = Scenario(
            description="Other",
            scenario_type=ScenarioType.BUDGET,
            tenant_id=admin_actor.tenant_id,
            assumptions=None,
        )
        await repository.save(scenario1)
        await repository.save(scenario2)

        use_case = ListScenarioUseCase(repository)
        input_dto = ListRequestInputDTO(
            actor=admin_actor, filters={"description": "Target"}
        )

        result = await use_case.execute(input_dto)

        assert result.meta.total_items == 1
        assert len(result.data) == 1
        assert result.data[0].description == "Target"
