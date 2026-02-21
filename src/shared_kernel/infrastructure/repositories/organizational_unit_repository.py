from uuid import UUID

from sqlalchemy.orm import Session

from src.core.infrastructure.repository import SQLAlchemyRepository
from src.shared_kernel.domain.entities import OrganizationalUnit
from src.shared_kernel.domain.repositories import IOrganizationalUnitRepository
from src.shared_kernel.infrastructure.mappers import OrganizationalUnitMapper
from src.shared_kernel.infrastructure.models import OrganizationalUnitModel


class OrganizationalUnitRepository(
    SQLAlchemyRepository[OrganizationalUnit, OrganizationalUnitModel],
    IOrganizationalUnitRepository,
):
    """
    Repository for manning OrganizationalUnit entities using SQLAlchemy

    :param session: SQLAlchemy session.
    """

    def __init__(self, session: Session):
        """
        Initialize the OrganizationalUnitRepository with a SQLAlchemy session.

        :param session: SQLAlchemy session.
        """

        super().__init__(
            session,
            OrganizationalUnitModel,
            mapper=OrganizationalUnitMapper,
        )

    def get_by_parent_id(
        self,
        parent_id: UUID | None,
        tenant_id: UUID | None,
    ) -> list[OrganizationalUnit]:
        """
        Get OrganizationalUnits by parent_id using SQLAlchemy
        """

        query = self._session.query(self._model_cls).filter_by(
            parent_id=parent_id,
            tenant_id=tenant_id,
        )
        query = query.order_by(self._model_cls.code)

        models = query.all()

        return [self._mapper.to_entity(model) for model in models]
