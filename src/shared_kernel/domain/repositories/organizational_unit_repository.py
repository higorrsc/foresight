from abc import abstractmethod
from uuid import UUID

from src.core.domain import AbstractRepository
from src.shared_kernel.domain.entities import OrganizationalUnit


class IOrganizationalUnitRepository(AbstractRepository[OrganizationalUnit]):
    """
    Interface for the Organizational Unit Repository.
    """

    @abstractmethod
    async def get_by_parent_id(
        self,
        parent_id: UUID,
        tenant_id: UUID,
    ) -> list[OrganizationalUnit]:
        """
        Get organizational units by parent ID.
        """

        raise NotImplementedError  # pragma: no cover
