from src.core.domain import AbstractRepository
from src.shared_kernel.domain.entities import FinancialScenario


class IFinancialScenarioRepository(AbstractRepository[FinancialScenario]):
    """
    Interface for the Financial Scenario Repository.
    """
