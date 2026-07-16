from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.infrastructure.repository import SQLAlchemyRepository
from src.tenant_management.domain.entities import Plan
from src.tenant_management.domain.repositories.plan_repository import IPlanRepository
from src.tenant_management.infrastructure.mappers import PlanMapper
from src.tenant_management.infrastructure.models import PlanModel


class PlanRepository(SQLAlchemyRepository[Plan, PlanModel], IPlanRepository):
    """
    Repository for managing Plan entities using SQLAlchemy.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the PlanRepository with a SQLAlchemy session.

        :param session: SQLAlchemy session.
        """

        super().__init__(
            session,
            PlanModel,
            mapper=PlanMapper(),
        )

    async def get_by_name(self, name: str) -> Plan | None:
        """
        Finds a plan by its name.
        """

        stmt = select(self._model_cls).where(
            self._model_cls.name == name,
        )

        result = await self._session.execute(stmt)
        model = result.unique().scalar_one_or_none()

        return self._mapper.to_entity(model) if model else None
