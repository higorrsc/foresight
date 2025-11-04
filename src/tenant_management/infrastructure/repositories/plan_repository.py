from sqlalchemy.orm import Session

from src.shared_kernel.infrastructure.repositories._shared import SQLAlchemyRepository
from src.tenant_management.domain.entities import Plan
from src.tenant_management.infrastructure.mappers import PlanMapper
from src.tenant_management.infrastructure.models import PlanModel


class PlanRepository(SQLAlchemyRepository[Plan, PlanModel]):
    """
    Repository for managing Plan entities using SQLAlchemy.
    """

    def __init__(self, session: Session):
        """
        Initialize the PlanRepository with a SQLAlchemy session.

        :param session: SQLAlchemy session.
        """

        super().__init__(session, PlanModel, mapper=PlanMapper)
