from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.shared_kernel.infrastructure.repositories._shared import SQLAlchemyRepository
from src.tenant_management.domain.entities import Plan
from src.tenant_management.domain.repositories.plan_repository import IPlanRepository
from src.tenant_management.infrastructure.mappers import PlanMapper
from src.tenant_management.infrastructure.models import PlanModel


class PlanRepository(SQLAlchemyRepository[Plan, PlanModel], IPlanRepository):
    """
    Repository for managing Plan entities using SQLAlchemy.
    """

    def __init__(self, session: Session):
        """
        Initialize the PlanRepository with a SQLAlchemy session.

        :param session: SQLAlchemy session.
        """

        super().__init__(session, PlanModel, mapper=PlanMapper)

    def get_by_name(self, name: str) -> Optional[Plan]:
        """
        Finds a plan by its name.
        """

        stmt = select(self._model_cls).filter_by(name=name)
        model = self._session.scalars(stmt).first()
        return self._mapper.to_entity(model) if model else None
