from src.core.application.use_cases.queries import GenericGetByIdUseCase
from src.shared_kernel.application.use_cases.financial_scenario import (
    FinancialScenarioNotFoundError,
)
from src.shared_kernel.domain.entities import FinancialScenario
from src.shared_kernel.domain.repositories import IFinancialScenarioRepository


class GetFinancialScenarioByIdUseCase(GenericGetByIdUseCase[FinancialScenario]):
    """
    Use case for getting a financial scenario by its ID.
    """

    def __init__(self, repository: IFinancialScenarioRepository) -> None:
        """
        Initialize the get by id use case.
        """

        super().__init__(
            repository,
            FinancialScenarioNotFoundError,
            "Financial Scenario with given ID not found.",
        )
