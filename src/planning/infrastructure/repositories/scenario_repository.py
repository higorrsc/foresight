from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.infrastructure.repository import SQLAlchemyRepository
from src.planning.domain.entities import Scenario
from src.planning.domain.repositories import IScenarioRepository
from src.planning.infrastructure.mappers import ScenarioMapper
from src.planning.infrastructure.models import ScenarioModel


class ScenarioRepository(
    SQLAlchemyRepository[Scenario, ScenarioModel],
    IScenarioRepository,
):
    """
    Repository for managing Scenario entities using SQLAlchemy.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the ScenarioRepository with a SQLAlchemy session.

        :param session: SQLAlchemy session.
        """

        super().__init__(
            session,
            ScenarioModel,
            ScenarioMapper(),
        )

    def _get_base_query(self):
        """Hook to allow children repos add eager loads (options)."""

        return select(self._model_cls).options(
            selectinload(self._model_cls.exchange_rates)
        )
