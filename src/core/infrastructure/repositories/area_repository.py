from sqlalchemy.orm import Session

from src.core.domain.entities import Area
from src.core.infrastructure.mappers import AreaMapper
from src.core.infrastructure.models import AreaModel
from src.core.infrastructure.repositories._shared import SQLAlchemyRepository


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
