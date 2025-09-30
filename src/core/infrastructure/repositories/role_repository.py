from sqlalchemy.orm import Session

from src.core.domain.entities import Role
from src.core.infrastructure.mappers import RoleMapper
from src.core.infrastructure.models import RoleModel
from src.core.infrastructure.repositories._shared import SQLAlchemyRepository


class RoleRepository(SQLAlchemyRepository[Role, RoleModel]):
    """
    Repository for managing Role entities using SQLAlchemy.
    """

    def __init__(self, session: Session):
        """
        Initialize the RoleRepository with a SQLAlchemy session.

        :param session: SQLAlchemy session.
        """

        super().__init__(session, RoleModel, mapper=RoleMapper)
