from abc import abstractmethod
from typing import List, Optional
from uuid import UUID

from src.shared_kernel.domain._shared import AbstractRepository
from src.shared_kernel.domain.entities import OrganizationalUnit


class IOrganizationalUnitRepository(AbstractRepository[OrganizationalUnit]):
    """
    Interface for the Organizational Unit Repository.
    """

    @abstractmethod
    def get_by_parent_id(
        self,
        parent_id: Optional[UUID],
        tenant_id: Optional[UUID],
    ) -> List[OrganizationalUnit]:
        """
        Get organizational units by parent ID.
        """

        raise NotImplementedError  # pragma: no cover
