from src.core.application.use_cases.queries import GenericListUseCase
from src.shared_kernel.domain.entities import FinancialScenario
from src.shared_kernel.domain.repositories import IFinancialScenarioRepository


class ListFinancialScenarioUseCase(GenericListUseCase[FinancialScenario]):
    """
    Use case for listing financial scenarios.
    """

    def __init__(self, repository: IFinancialScenarioRepository) -> None:
        """
        Initialize the list use case.

        :param repository: The repository to use for listing financial scenarios.
        """

        super().__init__(repository)
