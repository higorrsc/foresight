from abc import abstractmethod
from uuid import UUID

from src.core.domain.repository import AbstractRepository
from src.tenant_management.domain.entities.tenant import Tenant


class ITenantRepository(AbstractRepository[Tenant]):
    """
    Interface (contract) for the Tenant repository.
    """

    @abstractmethod
    def get_by_id_global(self, tenant_id: UUID) -> Tenant | None:
        """
        Finds a tenant by its unique id.
        """

        raise NotImplementedError  # pragma: no cover
