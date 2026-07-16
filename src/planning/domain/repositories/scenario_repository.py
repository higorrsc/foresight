from src.core.domain import AbstractRepository
from src.planning.domain.entities import Scenario


class IScenarioRepository(AbstractRepository[Scenario]):
    """
    Interface for the Scenario Repository.
    """
