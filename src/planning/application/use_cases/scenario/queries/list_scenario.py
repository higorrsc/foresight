from src.core.application.use_cases.queries import GenericListUseCase
from src.identity_access_management.domain.constants.permissions import AppPermission
from src.planning.domain.entities import Scenario
from src.planning.domain.repositories import IScenarioRepository


class ListScenarioUseCase(GenericListUseCase[Scenario]):
    """
    Use case for listing financial scenarios.
    """

    def __init__(self, repository: IScenarioRepository) -> None:
        """
        Initialize the list use case.

        :param repository: The repository to use for listing financial scenarios.
        """

        super().__init__(
            repository,
            AppPermission.FINANCIAL_SCENARIO_READ,
        )
