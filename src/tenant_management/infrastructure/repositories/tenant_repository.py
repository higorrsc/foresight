from sqlalchemy.orm import Session

from src.shared_kernel.infrastructure.repositories._shared import SQLAlchemyRepository
from src.tenant_management.domain.entities import Tenant
from src.tenant_management.infrastructure.mappers import TenantMapper
from src.tenant_management.infrastructure.models import TenantModel


class TenantRepository(SQLAlchemyRepository[Tenant, TenantModel]):
    """
    Repository for managing Tenant entities using SQLAlchemy.
    """

    def __init__(self, session: Session):
        """
        Initialize the TenantRepository with a SQLAlchemy session.

        :param session: SQLAlchemy session.
        """

        super().__init__(session, TenantModel, mapper=TenantMapper)
