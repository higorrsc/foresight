from sqlalchemy.orm import Session

from src.core.infrastructure.repository import SQLAlchemyRepository
from src.planning.domain.entities import ExchangeRate
from src.planning.domain.repositories import IExchangeRateRepository
from src.planning.infrastructure.mappers import ExchangeRateMapper
from src.planning.infrastructure.models import ExchangeRateModel


class ExchangeRateRepository(
    SQLAlchemyRepository[ExchangeRate, ExchangeRateModel],
    IExchangeRateRepository,
):
    """
    Repository for managing ExchangeRate entities using SQLAlchemy.
    """

    def __init__(self, session: Session):
        """
        Initialize the ExchangeRateRepository with a SQLAlchemy session.

        :param session: SQLAlchemy session.
        """

        super().__init__(session, ExchangeRateModel, ExchangeRateMapper())
