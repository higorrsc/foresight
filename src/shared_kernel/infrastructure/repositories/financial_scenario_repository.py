from sqlalchemy.orm import Session

from src.core.infrastructure.repository import SQLAlchemyRepository
from src.shared_kernel.domain.entities import FinancialScenario
from src.shared_kernel.domain.repositories import IFinancialScenarioRepository
from src.shared_kernel.infrastructure.mappers import (
    FinancialScenarioMapper,
)
from src.shared_kernel.infrastructure.models import (
    FinancialScenarioModel,
)


class FinancialScenarioRepository(
    SQLAlchemyRepository[FinancialScenario, FinancialScenarioModel],
    IFinancialScenarioRepository,
):
    """
    Repository for managing FinancialScenario entities using SQLAlchemy.
    """

    def __init__(self, session: Session):
        """
        Initialize the FinancialScenarioRepository with a SQLAlchemy session.

        :param session: SQLAlchemy session.
        """

        super().__init__(session, FinancialScenarioModel, FinancialScenarioMapper())
