from src.core.application.use_cases.commands import GenericRestoreUseCase
from src.identity_access_management.domain.constants import AppPermission
from src.shared_kernel.application.use_cases.financial_scenario import (
    FinancialScenarioNotFoundError,
)
from src.shared_kernel.domain.entities import FinancialScenario
from src.shared_kernel.domain.repositories import IFinancialScenarioRepository


class RestoreFinancialScenarioUseCase(GenericRestoreUseCase[FinancialScenario]):
    """
    Use case for deleting an Financial Scenario.
    """

    def __init__(self, repository: IFinancialScenarioRepository) -> None:
        """
        Initialize the RestoreFinancialScenarioUseCase.
        """

        super().__init__(
            repository,
            AppPermission.FINANCIAL_SCENARIO_DELETE,
            FinancialScenarioNotFoundError,
            "Financial Scenario with given ID not found.",
        )
