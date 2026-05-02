from src.identity_access_management.domain.entities import User
from src.shared_kernel.application.use_cases.financial_scenario.commands import (
    CreateFinancialScenarioInputDTO,
    CreateFinancialScenarioUseCase,
)
from src.shared_kernel.domain.entities import ScenarioType
from tests.fakes.in_memory_repository import FinancialScenarioInMemoryRepository


class TestCreateFinancialScenarioUseCase:
    """
    Test suite for the CreateFinancialScenarioUseCase.
    """

    def test_create_financial_scenario_success(self, admin_actor: User):
        """
        Test successful creation of a financial scenario.
        """
        repository = FinancialScenarioInMemoryRepository()
        use_case = CreateFinancialScenarioUseCase(repository)

        input_dto = CreateFinancialScenarioInputDTO(
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
