from abc import abstractmethod
from typing import Optional
from uuid import UUID

from src.identity_access_management.domain.entities import Role
from src.shared_kernel.domain._shared import AbstractRepository


class IRoleRepository(AbstractRepository[Role]):
    """
    Interface for the Role Repository.
    """

    @abstractmethod
    def get_by_name(
        self,
        name: str,
        tenant_id: Optional[UUID],
    ) -> Optional[Role]:
        """
        Get a role by its name.
        """

        raise NotImplementedError  # pragma: no cover
