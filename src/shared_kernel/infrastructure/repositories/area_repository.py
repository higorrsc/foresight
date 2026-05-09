from sqlalchemy.ext.asyncio import AsyncSession

from src.core.infrastructure.repository import SQLAlchemyRepository
from src.shared_kernel.domain.entities import Area
from src.shared_kernel.domain.repositories import IAreaRepository
from src.shared_kernel.infrastructure.mappers import AreaMapper
from src.shared_kernel.infrastructure.models import AreaModel


class AreaRepository(
    SQLAlchemyRepository[Area, AreaModel],
    IAreaRepository,
):
    """
    Repository for managing Area entities using SQLAlchemy.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the AreaRepository with a SQLAlchemy session.

        :param session: SQLAlchemy session.
        """

        super().__init__(
            session,
            AreaModel,
            AreaMapper(),
        )
