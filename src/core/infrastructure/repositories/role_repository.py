from typing import Optional

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

    def get_by_name(self, name: str) -> Optional[Role]:
        """
        Get a role by its name.
        """

        model = self._session.query(self._model_cls).filter_by(name=name).first()
        return self._mapper.to_entity(model) if model else None
