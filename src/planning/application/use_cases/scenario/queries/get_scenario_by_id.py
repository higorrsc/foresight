from src.core.application.use_cases.queries import GenericGetByIdUseCase
from src.identity_access_management.domain.constants import AppPermission
from src.planning.domain.entities import Scenario
from src.planning.domain.exceptions import ScenarioNotFoundError
from src.planning.domain.repositories import IScenarioRepository


class GetScenarioByIdUseCase(GenericGetByIdUseCase[Scenario]):
    """
    Use case for getting a financial scenario by its ID.
    """

    def __init__(self, repository: IScenarioRepository) -> None:
        """
        Initialize the get by id use case.
        """

        super().__init__(
            repository,
            AppPermission.SCENARIO_READ,
            ScenarioNotFoundError,
            "Scenario with given ID not found.",
        )
