from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.identity_access_management.domain.entities import Role
from src.identity_access_management.domain.repositories import IRoleRepository
from src.identity_access_management.infrastructure.mappers import RoleMapper
from src.identity_access_management.infrastructure.models import RoleModel
from src.shared_kernel.infrastructure.repositories._shared import SQLAlchemyRepository


class RoleRepository(
    SQLAlchemyRepository[Role, RoleModel],
    IRoleRepository,
):
    """
    Repository for managing Role entities using SQLAlchemy.
    """

    def __init__(self, session: Session):
        """
        Initialize the RoleRepository with a SQLAlchemy session.

        :param session: SQLAlchemy session.
        """

        super().__init__(session, RoleModel, mapper=RoleMapper)

    def get_by_name(
        self,
        name: str,
        tenant_id: Optional[UUID],
    ) -> Optional[Role]:
        """
        Get a role by its name.
        """

        model = (
            self._session.query(self._model_cls)
            .filter_by(name=name, tenant_id=tenant_id)
            .first()
        )
        return self._mapper.to_entity(model) if model else None
