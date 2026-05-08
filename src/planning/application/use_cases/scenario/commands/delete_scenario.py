from src.core.application.use_cases.commands import GenericDeleteUseCase
from src.identity_access_management.domain.constants import AppPermission
from src.planning.domain.entities import Scenario
from src.planning.domain.exceptions import ScenarioNotFoundError
from src.planning.domain.repositories import IScenarioRepository


class DeleteScenarioUseCase(GenericDeleteUseCase[Scenario]):
    """
    Use case for deleting an Scenario.
    """

    def __init__(self, repository: IScenarioRepository) -> None:
        """
        Initialize the DeleteScenarioUseCase.
        """

        super().__init__(
            repository,
            AppPermission.SCENARIO_DELETE,
            ScenarioNotFoundError,
            "Scenario with given ID not found.",
        )
