from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.core.infrastructure.repository import SQLAlchemyRepository
from src.tenant_management.domain.entities import Tenant
from src.tenant_management.domain.repositories import ITenantRepository
from src.tenant_management.infrastructure.mappers import TenantMapper
from src.tenant_management.infrastructure.models import TenantModel


class TenantRepository(SQLAlchemyRepository[Tenant, TenantModel], ITenantRepository):
    """
    Repository for managing Tenant entities using SQLAlchemy.
    """

    def __init__(self, session: Session):
        """
        Initialize the TenantRepository with a SQLAlchemy session.

        :param session: SQLAlchemy session.
        """

        super().__init__(session, TenantModel, mapper=TenantMapper)

    def get_by_id_global(self, tenant_id: UUID) -> Optional[Tenant]:
        """
        Finds a tenant by its unique id.
        """

        model = self._session.get(self._model_cls, tenant_id)
        return self._mapper.to_entity(model) if model else None
