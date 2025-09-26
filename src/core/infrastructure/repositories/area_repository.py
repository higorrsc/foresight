from sqlalchemy.orm import Session

from core.domain.entities import Area
from core.infrastructure.mappers import AreaMapper
from core.infrastructure.models import AreaModel
from core.infrastructure.repositories import SQLAlchemyRepository


class AreaRepository(SQLAlchemyRepository[Area, AreaModel]):
    """
    Repository for managing Area entities using SQLAlchemy.
    """

    def __init__(self, session: Session):
        """
        Initialize the AreaRepository with a SQLAlchemy session.

        :param session: SQLAlchemy session.
        """

        super().__init__(session, AreaModel, mapper=AreaMapper)
