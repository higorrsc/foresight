from src.shared_kernel.domain._shared.repository import AbstractRepository
from src.tenant_management.domain.entities.tenant import Tenant


class ITenantRepository(AbstractRepository[Tenant]):
    """
    Interface (contract) for the Tenant repository.
    """
