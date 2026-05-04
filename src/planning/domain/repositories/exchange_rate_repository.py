from src.core.domain import AbstractRepository
from src.planning.domain.entities import ExchangeRate


class IExchangeRateRepository(AbstractRepository[ExchangeRate]):
    """
    Interface for the Exchange Rate Repository.
    """
