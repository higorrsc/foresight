from src.core.application.use_cases.queries import GenericGetByIdUseCase
from src.identity_access_management.domain.constants import AppPermission
from src.planning.domain.entities import Scenario
from src.planning.domain.exceptions import ScenarioNotFoundError
from src.planning.domain.repositories import IScenarioRepository


class GetScenarioDetailsUseCase(GenericGetByIdUseCase[Scenario]):
    """
    Use case for getting detailed information about a financial scenario.
    """

    def __init__(self, repository: IScenarioRepository) -> None:
        """
        Initialize the get details use case.
        """

        super().__init__(
            repository,
            AppPermission.SCENARIO_READ,
            ScenarioNotFoundError,
            "Scenario with given ID not found.",
        )
